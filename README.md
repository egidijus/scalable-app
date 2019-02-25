# modern ansible, AWS, ECS fargate "serverless" scalable app

# What is this?
This solution will:
1. Build a docker image locally with a basic python app.
1. Create a VPC with public routes and security groups.
1. Creates relevant IAM Roles for ECS/FARGATE.
1. Push docker image to AWS ECR.
1. Create an AWS ECS cluster and service and task.
1. Start ECS cluster task based on your container.
1. Attach the ECS FARGATE cluster to an AWS ELB for dynamic scaling.
1. You can scale number of nodes you want to run by changing `size_of_cluster: 2` in `./vars/all.yml`
1. This also puts logs in to AWS Cloudwatch.




Find conatiners accessible behing the ELB
```
$▶ dig tomato.cat

; <<>> DiG 9.11.3-1ubuntu1.3-Ubuntu <<>> tomato.cat
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 13650
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1452
;; QUESTION SECTION:
;tomato.cat.                    IN      A

;; ANSWER SECTION:
tomato.cat.             60      IN      A       52.209.168.210
tomato.cat.             60      IN      A       54.76.137.186
```

## Access
ELB entrance is via  http://tomato.cat
Health endpoint : http://tomato.cat/_health


## You will need

```
ansible
awscli
boto
botocore
boto3
docker
docker-py
docker-compose
```




# Considerations assumptions and caveats
This solution does not cover:
## Discovery:
We could use AWS R53 DNS with a "local" zone setup and registering all the resources in to that zone. Or we could use something like HashiCorp Consul which we would ship with the container.

## Complex container:
This is a very basic docker application container. We could have a service supervisor in the container like s6-overlay and have the app run nginx, uwsgi python and varnish with consul-template or consul env for dynamically loading and reloading configuration changes.

## CI:
This does not include test or test runner, but it should be easy to plug in steps in to a CI pipeline.

## Monitoring and alerting:
We could solve this with AWS Cloudwatch metrics, create an alarm on AWS ELB 40x and 50x responses, alarm publishes a notification to AWS SNS, AWS SNS is configured to a pagerduty endpoint and would call the on-call engineer.

## Logging:
We would ship our logs to Logstash (either directly or by using a shipper that supports back-off and retry like Filebeat/Functionbeat) for processing. Logstash would parse logs and then ship to Elasticsearch cluster. We would have Dead Letter Queue for any logs that failed to be processed, store these logs in S3. This way we have never lose any log messages, and we could update the Logstash templates to improve parsing. Alternatively we could write logs directly in to AWS Cloudwatch Logs streams.

## Metrics:
We would use a lightweight metric shipper like Telegraf (from the Tick stack). Or we can create custom metrics and write directly in to AWS Cloudwatch.

## Backups:
The application and the configuration is all in the code. The database schema and migrations would live in code. Application would be designed to be stateless. We trust RDS to be resilient, we take nightly snapshots and have point-in-time recover. Static files would be stored in S3.

## VPC and environment isolation:
I am assuming that staging/test/uat environment are already configured and we are only concerned to deploying to one environment.


# Instructions
You will need to have *docker* and *docker-compose* installed locally, these instructions are for a linux machine.
You will need to have an AWS R53 zone setup and under your control, because we will be changing some A records. It is advisable you review the code carefully before running this.


On your workstation, in the terminal:
```
git clone git@github.com:egidijus/scalable-app.git && cd scalable-app
```

Let's build the project:
```
docker-compose build
```

Let's test the project locally:
```
docker-compose up
```
We should be able to access the app on http://localhost:8448 and the health endpoint on http://localhost:8448/_health .

Before we deploy this to AWS with ECS, we need to change some variables.
Create a file `./vars/secret.yml` and add your AWS access keys, like this:
```
key_id: AAAAAAAAAAA
access_key: AAAAAAAAAAAAAAAAAA
```
Ensure that you have the correct profile as your default profile in `~/.aws/credentials` .
We also want to export our keys to the current shell environment like this:

```
echo export AWS_ACCESS_KEY_ID="AAAAAAAAAAA"
echo export AWS_SECRET_ACCESS_KEY="AAAAAAAAAAAAAAAAAA"
```

In my example, I own the domain tomato.cat so I setup the `dns_zone` to `tomato.cat` in `./vars/all.yml`.


activate local python env:
```
virtualenv --no-site-packages -p python3 venv
. ./venv/bin/activate

pip install -r requirements.txt

ansible-playbook provision-and-deploy.yml -vv
```


## Technologies mentioned and references




## TODO


