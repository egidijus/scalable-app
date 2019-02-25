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


