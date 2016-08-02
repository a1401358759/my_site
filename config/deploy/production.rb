set :deploy_to, "/home/cloud/#{fetch :application}"
set :branch, 'master'

server '172.16.11.17', roles: [:db]


