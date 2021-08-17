from setuptools import setup

setup(
   name= 'mkad',
   version= '1.0',
   description= 'MKAD distance calculator',
   url= 'https://github.com/gabhcosta/mkad',
   author= 'Gabriel Costa',
   author_email= 'gabrielsantos.ghsc@gmail.com',
   packages= ['mkad'],
   python_requires='<3.9',
   install_requires= [
       'pandas==1.3.1',
       'shapely==1.7.1',
       'vincenty==0.1.4',
       'flask==2.0.1',
       'flask_restful==0.3.9',
       'requests==2.26.0'
    ], 
)