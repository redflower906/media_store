var plan = require('flightplan');

var config = {
  projectDir: '/opt/media_v2/',
  keepReleases: 3
};

// plan.target('staging', {
//   host: '10.101.10.49', // 
//   username: process.env.USER,
//   agent: process.env.SSH_AUTH_SOCK
// },
// {
//   // Setting this to false on the command line will allow
//   // the deployment to proceed even if there are uncommitted
//   // files on the file system. eg:
//   // fly deploy:staging --gitCheck=false
//   gitCheck: true
// });

plan.target('production', {
  host: '10.37.6.50', // vm650
  username: process.env.USER,
  agent: process.env.SSH_AUTH_SOCK,
},
{
  // Shouldn't be overridden, so please don't try.
  gitCheck: true
});

// Check if there are files that have not been committed to git. This stops
// us from deploying code in an inconsistent state. It also prevents slapdash
// changes from being deployed without a log of who added them in github. Not
// fool proof, but better than nothing.
plan.local('deploy', function(local) {
  if (plan.runtime.target === 'production' || plan.runtime.options.gitCheck) {
    local.log('checking git status...');
    var result = local.exec('git status --porcelain', {silent: true});

    if (result.stdout) {
      local.log(result.stdout);
      plan.abort('Uncommited files found, see list above');
    }
  } else {
    local.log('skipping git check!!!');
  }
});


plan.remote('deploy', function(remote) {
  config.deployTo = config.projectDir + '/releases/' + (new Date().getTime());
  remote.log('Creating webroot');
  remote.exec('mkdir -p ' + config.deployTo);
});

// Gets a list of files that git knows about and sends them to the
// target.
plan.local('deploy', function (local) {
  local.log('Transferring website files');
  var files = local.git('ls-files', {silent: true});
  local.transfer(files, config.deployTo + '/');
});

plan.remote('deploy', function(remote) {
  remote.log('Setup necessary symbolic links');
  remote.exec('ln -s /opt/media_v2/local_settings.py ' + config.deployTo + '/local_settings.py');
  remote.exec('ln -s /opt/media_v2/databasesettings.py ' + config.deployTo + '/databasesettings.py');
});

// plan.remote('deploy', function(remote) {
//   remote.log('collectstatic files');
//   remote.exec('cd '+ config.deployTo + '; /opt/djangoprojects/resourcematrix/venv/bin/python manage.py collectstatic --noinput');
// });

// plan.remote('deploy', function(remote) {
//   remote.log('compress static files');
//   remote.exec('cd '+ config.deployTo + '; /opt/djangoprojects/resourcematrix/venv/bin/python manage.py compress');
// });

plan.remote('deploy',function (remote) {
  remote.log('Linking to new release');
  remote.exec('ln -nfs ' + config.deployTo + ' ' +
    config.projectDir + '/current');

  remote.log('Checking for stale releases');
  var releases = getReleases(remote);

  if (releases.length > config.keepReleases) {
    var removeCount = releases.length - config.keepReleases;
    remote.log('Removing ' + removeCount + ' stale release(s)');

    releases = releases.slice(0, removeCount);
    releases = releases.map(function (item) {
      return config.projectDir + '/releases/' + item;
      });

    remote.exec('rm -rf ' + releases.join(' '));
  }
});

plan.remote('deploy', function(remote) {
  remote.log('Restart services...');
  remote.log("we don't have sudo, so log into the server and run the following as root");
  remote.log("cd " + config.projectDir + '/current');
  remote.log("source " + config.projectDir + "/venv/bin/activate");
  remote.log("if you've updated any python modules in requirements.txt, run: sudo pip install -r requirements.txt")
  remote.log("python manage.py migrate --database=default_root");
  remote.log("python manage.py collectstatic");
  remote.log("python manage.py compress");
  remote.log("/etc/init.d/resourcematrix restart");
});


plan.remote('rollback', function(remote) {
  remote.log('Rolling back release');
  var releases = getReleases(remote);
  if (releases.length > 1) {
    var oldCurrent = releases.pop();
    var newCurrent = releases.pop();
    remote.log('Linking current to ' + newCurrent);
    remote.exec('ln -nfs ' + config.projectDir + '/releases/' + newCurrent + ' '
      + config.projectDir + '/current');

    remote.log('Removing ' + oldCurrent);
    remote.exec('rm -rf ' + config.projectDir + '/releases/' + oldCurrent);
  }

});

plan.remote(['default','uptime'], function(remote) {
  remote.exec('uptime');
});


function getReleases(remote) {
  var releases = remote.exec('ls ' + config.projectDir +
    '/releases', {silent: true});

  if (releases.code === 0) {
    releases = releases.stdout.trim().split('\n');
    return releases;
  }

  return [];
}