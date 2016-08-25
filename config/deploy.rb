set :application, 'my_site'
set :repo_url, 'git@github.com:a1401358759/my_site.git'
set :ssh_options, {user: 'root'}
set :scm, :git
set :keep_releases, 5
set :stages, %w(master,staging production)
set :default_stage, "master"

namespace :deploy do
  after :updated, :config_files do
    on roles(:all) do
      execute "ln -s #{fetch :deploy_to}/shared/log #{fetch :release_path}/log"
      execute "cp /root/my_site-config/gunicorn.conf #{fetch :release_path}"
    end
  end

  after :updated, :migrate do
    on roles(:db) do
      within fetch(:release_path) do
        execute :python, "manage.py migrate"
      end
    end
  end

  after :published, :restart_web do
    on roles(:web) do
      within "#{fetch :deploy_to}/current" do
        execute :bash, "runserver.sh restart-web"
      end
    end
  end

end
