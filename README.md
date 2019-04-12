# snapshotalyzer-30000
Demo project to manage AWS EC2 instance snapshots

## About
This project is a demo, and uses boto3 to manage AWS EC2 instance snapshots.

## Configuring
snapshotalyzer uses the configuration file created by the AWS cli. e.g.

```
aws configure --profile snapshotalyzer
```

## Running
```
pipenv run python snapshotalyzer/shotty.py <COMMAND> <--project=PROJECT>
```
*COMMAND* is list, start, or stop 
*PROJECT* is the value for the instance Project tag. PROJECT is optional. If PROJECT is ommitted, the COMMAND will be executed against all instances.
