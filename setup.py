from setuptools import setup

setup(
   name= 'mkad',
   version= '1.0',
   description= 'MKAD distance calculator',
   url= 'https://github.com/gabhcosta/mkad',
   author= 'Gabriel Costa',
   author_email= 'gabrielsantos.ghsc@gmail.com',
   packages= ['mkad'],
   python_requires='>=3.8',
   install_requires= [
       'pandas==1.3.1',
       'shapely==1.7.1',
    ], 
)