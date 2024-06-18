from BD.sqlite import BD
import json

bd = BD()

kp = True
# mhs = ['EOO','FOX','GOA','GWO','HBA','PSA','PSO','RSA','SCA','SHO','TDA','WOA']
mhs = ['GWO']

cantidad = 0

DS_actions = [
    'V1-STD', 'V1-COM', 'V1-PS', 'V1-ELIT',
    'V2-STD', 'V2-COM', 'V2-PS', 'V2-ELIT',
    'V3-STD', 'V3-COM', 'V3-PS', 'V3-ELIT',
    'V4-STD', 'V4-COM', 'V4-PS', 'V4-ELIT',
    'S1-STD', 'S1-COM', 'S1-PS', 'S1-ELIT',
    'S2-STD', 'S2-COM', 'S2-PS', 'S2-ELIT',
    'S3-STD', 'S3-COM', 'S3-PS', 'S3-ELIT',
    'S4-STD', 'S4-COM', 'S4-PS', 'S4-ELIT',
]

paramsML = json.dumps({
    'MinMax'        : 'min',
    'DS_actions'    : DS_actions,
    'gamma'         : 0.4,
    'policy'        : 'e-greedy',
    'qlAlphaType'   : 'static',
    'rewardType'    : 'withPenalty1',
    'stateQ'        : 2
})

if kp:
    # poblar ejecuciones SCP
    # instancias = bd.obtenerInstancias(f'''
    #                                   "knapPI_1_100_1000_1","knapPI_2_100_1000_1","knapPI_3_100_1000_1","knapPI_1_200_1000_1","knapPI_2_200_1000_1","knapPI_3_200_1000_1","knapPI_1_500_1000_1","knapPI_2_500_1000_1","knapPI_3_500_1000_1","knapPI_1_1000_1000_1","knapPI_2_1000_1000_1","knapPI_3_1000_1000_1","knapPI_1_2000_1000_1","knapPI_2_2000_1000_1","knapPI_3_2000_1000_1"
    #                                   ''')
    instancias = bd.obtenerInstancias(f'''
                                      "knapPI_1_100_1000_1"
                                      ''')
    iteraciones = 500
    experimentos = 1
    poblacion = 20
    for instancia in instancias:

        for mh in mhs:
            binarizaciones = ['S2-STD']
            for binarizacion in binarizaciones:
                
                data = {}
                data['experimento'] = f'{mh} {binarizacion}'
                data['MH']          = mh
                data['paramMH']     = f'iter:{str(iteraciones)},pop:{str(poblacion)},DS:{binarizacion},cros:0.9;mut:0.20'
                data['ML']          = ''
                data['paramML']     = ''
                data['ML_FS']       = ''
                data['paramML_FS']  = ''
                data['estado']      = 'pendiente'

                cantidad +=experimentos
                bd.insertarExperimentos(data, experimentos, instancia[0])


print("------------------------------------------------------------------")
print(f'Se ingresaron {cantidad} experimentos a la base de datos')
print("------------------------------------------------------------------")

