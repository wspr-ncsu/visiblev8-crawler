import connexion
import api
import webpage

def main():
    # create Flask/Connexion app
    app = connexion.App(__name__, specification_dir='openapi/')
    # add openapi specifications
    app.add_api('webpages_v1.yaml')
    app.add_api('openapi_v1.yaml')
    # start server
    app.run(port=8080)

if __name__ == '__main__':
    main()
