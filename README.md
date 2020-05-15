# wbm2git

grab "internet archive wayback machine" page versions and commit them as git history

### what for
if you are interested in the changes of a website text, you can be lucky if the [Wayback Machine](https://web.archive.org/) created snapshots in the past. 
To get an overview about the changes, wbm2git provides a simple way to save the snpashots from WBM into a git history, so you can view the differences between the several commits (using for example `meld` or just the Diff on Github etc.)

### how to use

```
  import wbm2git
  wbm2git.Run('https://example.com', '~/example_versions')
```

you need to have a global git user setup, if not so you need to provide name and email via config

```
  import wbm2git
  config = wbm2git.default_config
  config['git_user_name'] = 'fjodor'
  config['git_user_email'] = 'fjodor@example.com'
  wbm2git.Run('https://example.com', '~/example_versions')
```

this way you can also change other default configurations

```
  git_user_name='None',
  git_user_email='None',
  # the filename within the git repository
  filename='content.html',
  # select the part of the website you want to commit
  css_selector_content='#content',
  # if there is publishing date available for the content, create a selector here
  css_selector_time='#date',
```
