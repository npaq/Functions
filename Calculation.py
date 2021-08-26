import os
import sqlite3
import sys
import csv
from Functions.Data_handling import insertTable


# Calculation of radiological impact
# dose(doseType, ageGroup) = MAR * dilution * ARF * RF * DCF(doseType, ageGroup) (* q)
def radiologicalImpact(
    isotopes, scenarios, ARF_RF, DCF, MAR, dilution_coefficient, respiratory_flows, \
        ageGroups, unit, doseTypes, conn, tableName, colNames
    ):
    """
    - isotope [list] : list of isotopes. The list must be the same as the keys in ARF_RF, MAR and DCF
    - MAR [dictionary]: Material at risk
        Given by
        - isotope
        - scenario
        - unit
    - ARF_RF [dictionary] : Airborne Release Fraction (ARF) * Respirable Fraction (RF)
        Given by : 
        - isotope
        - building
        - unit
    - DCF [dictionary] : Dose coefficient factors
        Given by:
        - isotope
        - dose type (inhalation, thyroid, cloud shine, ground shine)
        - age group
    - dilution_coefficient [float] : this coefficient is linked to the unit for which the calculation is done
    - respiratory_flows [dictionary] : flows by age group
    - doseTypes [list] : list of dose type. The list must be the same as the keys in DCF
    - ageGroups [list] : list of age groups. The list must be the same as the keys in DCF
    - unit [string]: unit for which the calculation is done  
    - conn : connection to the output DB
    - tableName [string] : name of the result table
    - colNames [list] : name of the columns in the result table
    """
    # Result dictionary : row by row. dose is used to record the result into the table
    dose = {}
    dose["Unit"] = unit
    # Result dictionay : contains all the results. d is used to perform further calculations (sum, max etc)
    d = {}
     

    # Calcultation by scenario
    cursor = conn.cursor()
    for scenario in scenarios:
        dose["Scenario"] = scenario
        building = scenario.split("_",1)[0]
        # Calculation of the various contribution to the dose for each isotope
        for isotope in isotopes:
            dose["Isotope"] = isotope
            # Source term calculation
            #--------------------------
            # Source term calculation - casting MAR : string to float
            MAR_value = MAR.get((isotope, scenario, unit))
            MAR_value = MAR_value.replace(',', '.')
            MAR_value = float(MAR_value)
      
            # Source term : MAR * dilution * ARF
            dilution_coefficient = dilution_coefficient.replace(',', '.')
            ARF = ARF_RF.get((isotope, building, unit))
            ARF = ARF.replace(',', '.')
            sourceTerm =  float(MAR_value) * float(dilution_coefficient) * float(ARF)

            # Dose calculations : source term * DCF (* q) 
            #------------------------------------------------
            for doseType in doseTypes:
                for ageGroup in ageGroups:
                    h = DCF.get((isotope, ageGroup, doseType))
                    h = h.replace(',', '.')
                    h = float(h)
                    # Result in a dictionary (dose)
                    resultName = doseType + '_' + ageGroup
                    if 'shine' in doseType.split("_"):
                        dose[resultName] = sourceTerm * h
                    else:
                        q = respiratory_flows.get(ageGroup)
                        q = q.replace(',', '.')
                        q = float(q)
                        dose[resultName] = sourceTerm * h * q
                    d[unit, scenario, isotope, doseType, ageGroup] = dose[resultName]
                    # recording in the database
                    # --------------------------
                    # recording in the table result
                    r = [unit, scenario, isotope, doseType, ageGroup, dose[resultName]]
                    insertTable(conn, tableName, colNames, r)        
    conn.commit()

    return d




