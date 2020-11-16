# -*- coding: utf-8 -*-
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.build import Build


def get_server_instance():
    jenkins_url = 'http://47.94.161.105:8080/jenkins/'
    server = Jenkins(jenkins_url, username='op', password='bbmm_Smart2020')
    return server


server = get_server_instance()
print(server.version)
# print(server.get_jobs_list())
job = server['nginxtest']
res = job.invoke(build_params={'action': 'deploy'})




