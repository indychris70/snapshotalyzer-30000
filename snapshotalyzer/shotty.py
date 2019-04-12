
import boto3
import sys
import click

@click.command()

def list_instances():
    "List EC2 Instances"
    for i in ec2.instances.all():
        print(", ".join(
                            (
                            i.id, 
                            i.instance_type,
                            i.placement["AvailabilityZone"],
                            i.state['Name'],
                            i.public_dns_name
                            )
                        )
        )

if __name__ == '__main__':
    print(sys.argv)
    
    # setup
    session = boto3.Session(profile_name="snapshotalyzer")
    ec2 = session.resource('ec2')
    
    # script
    list_instances()
    