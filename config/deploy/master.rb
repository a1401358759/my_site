set :deploy_to, "/root/#{fetch :application}"
set :branch, 'master'

server '172.16.11.17', roles: [:web, :db]
