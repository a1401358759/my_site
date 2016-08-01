# config valid only for current version of Capistrano
lock '3.5.0'

set :application, 'my_site'
set :repo_url, 'git@github.com:a1401358759/my_site.git'
set :ssh_options, {user: 'root'}
set :scm, :git
set :keep_releases, 5
set :stages, %w(master)
set :default_stage, "master"

namespace :deploy do

  after :updated, :config_files do
    on roles(:all) do
      execute "ln -s #{fetch(:deploy_to)}/log #{fetch(:release_path)}/log"
      execute "cp /home/cloud/my_site/uwsgi.ini #{fetch(:release_path)}"
    end
  end

  after :updated, :minify do
    if fetch(:stage).to_s != "master"
      on roles(:all) do
        execute "for file in `find #{fetch(:release_path)}/static/css/*.css`;do cleancss -o $file $file > /dev/null 2>&1; done"
        execute "for file in `find #{fetch(:release_path)}/static/js/*.js`;do uglifyjs -c -m -o $file $file > /dev/null 2>&1; done"
      end
    end
  end

  after :updated, :migrate do
    on roles(:db) do
      within fetch(:release_path) do
        execute :python, "manage.py migrate"
      end
    end
  end

  after :published, :restart do
    on roles(:web) do
      within "#{fetch :deploy_to}/current" do
        execute :bash, "runserver.sh restart-web"
      end
    end
  end

end


