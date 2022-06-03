from setuptools import setup, find_packages

with open("LICENSE.txt", "r", encoding='utf-8') as fh:
    license_from_file = fh.read()
setup(
    name='demoscene-mrmarvel',
    version='0.1.1',
    packages=find_packages(where='src'),  # ,
    package_dir={'': 'src'},
    url='',
    license=license_from_file,
    author='Sergey Kulikov',
    author_email='seregakkk999@yandex.ru',
    description='Demo-scene for class work',
    install_requires=["cursor", "numpy", "fps-limiter"]
)
