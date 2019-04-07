"""
The config module allows the definition of the structure of your servo robot.

Configuration are written as Python dictionary so you can define/modify them programmatically.

Born on October 2017. Last Mod on January 2018

* motors: You specify all motors belonging to your robot. You have to define their number of servo and angle_limit.


"""

ergo_servo_config = {
    
    'motors': {
        'nuca1': {
            'servo': 1,
            'code': 'xdeg',
            'orientation': 'indirect',
            'offset':0,#positivo mirando hacia afuera
            'mid': 180,
            'amp': 95,
            #'min': 60,
            #'max': 250,	
        },
        'nuca2': {
            'servo': 2,
            'code': 'ydeg',
            'orientation': 'indirect',
            'offset':0,#positivo mirando hacia afuera
            'mid': 150,
            'amp': 70,
            #'min': 90,#150-60 antes estaba 75
            #'max': 230,	#150 + 80 antes 150
        },
        'nuca3': {
            'servo': 3,
            'code': 'thetadeg',
            'orientation': 'indirect',
            'offset':0,#positivo mirando hacia afuera
            'mid': 170,
            'amp': 30,
            #'min': 140,
            #'max': 200,	
        },

    }, # motors
}
