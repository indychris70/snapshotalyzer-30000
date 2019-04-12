
import boto3
import sys
import click

def hello_world():
    return "Hello World!!"

def filter_instances(project):
    instances = []
    
    if project:
        filters = [{"Name": "tag:Project", "Values": [project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    
    return instances 

############# DEFAULT COMMANDS #################################################
@click.group()
def cli():
    """Shotty manages snapshots"""

############# SNAPSHOT COMMANDS ################################################
@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""
    
## LIST SNAPSHOTS ##
@snapshots.command('list')
@click.option('--project', default=None, help="Only snapshots for project (tag Project:<name>)")
def list_snapshots(project):
    "List Snapshots of EC2 Volumes"
    
    instances = filter_instances(project)
        
    for i in instances:
        tags = { t["Key"]: t["Value"] for t in i.tags or [] }
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join(
                                    (
                                        v.id,
                                        i.id,
                                        s.id,
                                        s.state,
                                        s.progress,
                                        s.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                                        tags.get("Project", "<no Project>")
                                    )
                                )
                )
    return

############# VOLUMES COMMANDS #################################################
@cli.group('volumes')
def volumes():
    """Commands for volumes"""
    
## LIST INSTANCES ##
@volumes.command('list')
@click.option('--project', default=None, help="Only volumes for project (tag Project:<name>)")
def list_volumes(project):
    "List EC2 Volumes"
    
    instances = filter_instances(project)
        
    for i in instances:
        tags = { t["Key"]: t["Value"] for t in i.tags or [] }
        for v in i.volumes.all():
            print(", ".join(
                                (
                                    v.id,
                                    i.id, 
                                    v.state,
                                    str(v.size) + "GiB",
                                    v.encrypted and "Encrypted" or "Not Encrypted",
                                    tags.get("Project", "<no Project>")
                                )
                            )
            )
    return

############# INSTANCES COMMANDS ###############################################
@cli.group('instances')
def instances():
    """Commands for instances"""

## CREATE SNAPSHOTS ##
@instances.command("snapshot", help="Create snapshots of all volumes")
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def create_snapshots(project):
    "Create snapshots for EC2 instance volumes"
    instances = filter_instances(project)
        
    for i in instances:
        for v in i.volumes.all():
            print("Creating snapshot of {}".format(v.id))
            v.create_snapshot(Description="Created by Snapshotalyzer-30000")
            
    return

## LIST INSTANCES ##
@instances.command('list')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 Instances"
    
    instances = filter_instances(project)
        
    for i in instances:
        tags = { t["Key"]: t["Value"] for t in i.tags or [] }
        print(", ".join(
                            (
                            i.id, 
                            i.instance_type,
                            i.placement["AvailabilityZone"],
                            i.state['Name'],
                            i.public_dns_name,
                            tags.get("Project", "<no Project>")
                            )
                        )
        )
    return
    
## STOP INSTANCES ##
@instances.command('stop')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Stop EC2 Instances"
    
    instances = filter_instances(project)
        
    for i in instances:
        tags = { t["Key"]: t["Value"] for t in i.tags or [] }
        if i.state["Name"] != "stopped" and i.state["Name"] != "stopping":
            print("Stopping {} (id: {})...".format(tags.get("Project", "<no Project>"), i.id))
            i.stop()
        else:
            print("Instance {} (id: {}) is {}".format(tags.get("Project", "<no Project>"), i.id, i.state["Name"]))

## START INSTANCES ##
@instances.command('start')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Start EC2 Instances"
    
    instances = filter_instances(project)
        
    for i in instances:
        tags = { t["Key"]: t["Value"] for t in i.tags or [] }
        if i.state["Name"] != "running" and i.state["Name"] != "pending":
            print("Starting {} (id: {})...".format(tags.get("Project", "<no Project>"), i.id))
            i.start()
        else:
            print("Instance {} (id: {}) is {}.".format(tags.get("Project", "<no Project>"), i.id, i.state["Name"]))    
        
############################# MAIN SCRIPT ######################################
if __name__ == '__main__':
    
    # setup
    session = boto3.Session(profile_name="snapshotalyzer")
    ec2 = session.resource('ec2')
    
    # script
    cli()
    