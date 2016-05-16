Marketing website
=================

##Setting up your Dev Machine (Mac OS: Yosemite)
- Install the latest Xcode 6.1.1 from the Apple Mac App Store
- Open terminal
- Get command line tools. Run in terminal: `xcode-select --install`
- Install Homebrew.
```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
- Check Homebrew installation with `brew doctor`
- Install Python
```
brew install python
```
- Install Python packages needed to run the application
```
pip install -r requirements.txt
```

##Compile CSS

```
sudo gem install compass
gem install css_parser
cd /dir
compass build
compass watch
```

##To run locally

First, set this environment variable in your local machine
```
export MARKETING_APP_DEBUG=True
```

Run this on the terminal: `python application.py`

##To deploy to AWS


Copy the following lines to `<repo-dir>/.elasticbeanstalk/config`:
```
[global]
ApplicationName=marketing
AwsCredentialFile=~/.elasticbeanstalk/aws_credential_file
DevToolsEndpoint=git.elasticbeanstalk.us-east-1.amazonaws.com
EnvironmentName=marketing-env
EnvironmentTier=WebServer::Standard::1.0
EnvironmentType=LoadBalanced
InstanceProfileName=aws-elasticbeanstalk-ec2-role
OptionSettingFile=/Users/kingshy/DEV/Hello/marketing-website/.elasticbeanstalk/optionsettings.marketing-env
RdsEnabled=No
Region=us-east-1
ServiceEndpoint=https://elasticbeanstalk.us-east-1.amazonaws.com
SolutionStack=64bit Amazon Linux 2014.03 v1.0.4 running Python 2.7
```
remember to change `AwsCredentialFile` and `OptionSettingFile` with the correct path on your local machine.

run this inside your repo directory:
```
sh <path to unzipped EB CLI package>/AWSDevTools/Linux/AWSDevTools-RepositorySetup.sh
```

make sure that you have access to `eb` tools by setting the `PATH` variable

Then `chmod 600 .elasticbeanstalk/config` and run `eb status` to confirm everything is setup properly

```
export PATH=$PATH:<path to unzipped EB CLI package>/eb/macosx/python2.7
```

To test on staging, git checkout -b new_branch, comment out sslify in application.py and `git commit` those changes. **never merge that branch back to master**.

```
git add your-changes
git commit -m "very useful commit message"
git aws.push -e marketing-staging
```

To run the application locally, set this environment variable in your local machine
```
export SHARING_APP_DEBUG=True
export ROOT_DOMAIN=hello.is
export ROOT_CDN=hellocdn.net
export MEMCACHED_HOSTNAME=localhost
export MEMCACHED_PORT=11211
```
