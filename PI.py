from server_side import app

version = '0.1.0'

if __name__ == '__main__' :
    
    print('------------------------------------------------')
    print('Wandlab CV - version ' + version )
    print('------------------------------------------------')
    
    app.run( host='0.0.0.0', port=5001 )
