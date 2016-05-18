{{cookiecutter.app_name}}
=====

Start manually
--------------

In this current folder, launch: `api_hour -ac {{cookiecutter.app_name}}:Container`

Deploy using Ansible
--------------------

#. `ansible-playbook ansible/install.yml -i ansible/inventory`
#. Customize config files in /etc/{{cookiecutter.app_name}}/
#. Merge rsyslog config file
#. service {{cookiecutter.app_name}} start

Deploy new version using Ansible
--------------------------------

#. `ansible-playbook ansible/update.yml`

Manual install
--------------

#. Follow pythonz install doc: https://github.com/saghul/pythonz
#. pythonz install 3.5.1
#. cd /opt
#. Git clone your app here
#. cd /opt/{{cookiecutter.app_name}}/
#. /usr/local/pythonz/pythons/CPython-3.5.1/bin/pyvenv pyvenv
#. . pyvenv/bin/activate
#. pip install -r requirements.txt
#. cd /etc/init.d/ && ln -s /opt/{{cookiecutter.app_name}}/etc/init.d/{{cookiecutter.app_name}}
#. To define right boot order for your daemon (for example, your daemon needs PostgreSQL), customize file header of: /opt/{{cookiecutter.app_name}}/etc/default/{{cookiecutter.app_name}}
#. cd /etc/default/ && ln -s /opt/{{cookiecutter.app_name}}/etc/default/{{cookiecutter.app_name}}
#. update-rc.d {{cookiecutter.app_name}} defaults
#. cp -a /opt/{{cookiecutter.app_name}}/etc/{{cookiecutter.app_name}} /etc/
#. Adapt rsyslog and logrotate
#. For logrotate config file, apply the access rights: rw-r--r--
#. service {{cookiecutter.app_name}} start

To restart automatically daemon if it crashes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#. apt-get install monit
#. cd /etc/monit/conf.d/ && ln -s /opt/{{cookiecutter.app_name}}/etc/monit/conf.d/{{cookiecutter.app_name}}
#. service monit restart
