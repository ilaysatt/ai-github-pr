from setuptools import setup, find_packages
setup(name='ai-github-pr',
      description='AI GitHub pull request comment generator',
      version='1.0.0',
      url='https://github.com/ilaysatt/ai-github-pr',
      author='Ilay Sat',
      author_email='ilaysat@gmail.com',
      scripts=['scripts/ai-github-pr'],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License'
      ],
      install_requires=['pygithub>=2.0.0', 'openai>=1.5.0', 'python-dotenv', 'tiktoken'])
