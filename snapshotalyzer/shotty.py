
import boto3
import sys
import click

def filter_instances(project):
    instances = []
    
    if project:
        filters = [{"Name": "tag:Project", "Values": [project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    
    return instances 
    
@click.group()
def instances():
    """Commands for instances"""
    
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
        
if __name__ == '__main__':
    
    # setup
    session = boto3.Session(profile_name="snapshotalyzer")
    ec2 = session.resource('ec2')
    
    # script
    instances()
    