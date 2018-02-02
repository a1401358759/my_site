set :deploy_to, "/root/#{fetch :application}"
set :branch, 'master'

server '123.207.158.145', roles: [:web]
