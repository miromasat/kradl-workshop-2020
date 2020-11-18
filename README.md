### Set-up the environment
⋅⋅* 1A: Create a Cloud9 environment in us-east-1 to perform the rest of the lab
        1AA: Use us-east-1 for the rest of this lab for all resources
⋅⋅* 1B: Setup Maven: https://gist.github.com/sebsto/19b99f1fa1f32cae5d00#gistcomment-2394990
⋅⋅* 1C: Clone these repositories: 
        1CA: https://github.com/aws-samples/amazon-kinesis-replay.git and compile using mvn install
⋅⋅* 1D: Create an IAM user with no policies attached called nyc-taxi-user-<XX>
⋅⋅* 1E: Create an IAM role with S3 full access + Glue full access policies attached, called nyc-taxi-role-<XX>
⋅⋅* 1F: Create four S3 buckets, you will use in later stages, replace <XX> with your initials
        1FA: nyc-taxi-store-7a-<XX>
        1FB: nyc-taxi-store-7b-<XX>
        1FC: nyc-taxi-store-7c-<XX>
        1FD: nyc-taxi-store-7d-<XX>
        1FF: nyc-taxi-store-<XX>
        1FG: nyc-taxi-analyze-<XX>
### Create a kinesis-stream with 10 shards by default, replace <XX> with your initials
⋅⋅* kinesis-stream name: nyc-taxi-ingest-<XX>
### Create a kinesis-firehose to deliver data from kinesis stream into S3, replace <XX> with your initials
⋅⋅* 3A: name of the kinesis-firehose: nyc-taxi-deliver-<XX>
⋅⋅* 3B: source: nyc-taxi-ingest-<XX>
⋅⋅* 3C: destination: nyc-taxi-store-<XX>
⋅⋅* 3D: Test the delivery with the agent: java -jar amazon-kinesis-replay-1.0.jar -streamName nyc-taxi-ingest-<XX> -streamRegion us-east-1
### Crawl nyc-taxi-store-<XX> S3 bucket using (replace <XX> with your initials)
⋅⋅* 5A: a crawler to discover the schema: nyc-taxi-crawl-<XX>
⋅⋅* 5B: a glue role: nyc-taxi-crawl-role-<XX>
⋅⋅* 5C: a database name: nyc-taxi-database-<XX>
⋅⋅* 5D: run the crawler and obtain a table within this database, call it: nyc-taxi-table-<XX>
### Same query (total_amount of a trip under 5 USD) in 4 different ways:
⋅⋅* 7A: temporary on the ingest using Kinesis Analytics Application: -> S3 bucket for the destination -> create kinesis firehose for delivery into S3, point kinesis analytics into the firehose
        7AA: create a kinesis-analytics application: nyc-taxi-analyze-7a-<XX>
        7AB: connect kinesis-analytics application to kinesis-stream: nyc-taxi-ingest-<XX>
        7AC: discover the schema with the agent: java -jar amazon-kinesis-replay-1.0.jar -streamName nyc-taxi-ingest-<XX> -streamRegion us-east-1
        7AD: create a kinesis-firehose: nyc-taxi-deliver-7a-<XX> 
        7AE: deliver kinesis-firehose results into: nyc-taxi-store-7a-<XX>
        7AF: attach kinesis-analytics application to kinesis-firehose
⋅⋅* 7B: permanently on the ingest using Lambda Function 
        7BA: create a lambda function through Cloud9 from a blueprint kinesis-firehose-process-record (python2.7): nycTaxiProcess<XX>
        7BB: replace the lambda code with code provided
        7BC: create a kinesis-firehose: nyc-taxi-deliver-7b-<XX>
        7BD: deliver kinesis-firehose results into: nyc-taxi-store-7b-<XX>
        7BE: attach the function to this new kinesis-firehose and test the delivery using the agent: java -jar amazon-kinesis-replay-1.0.jar -streamName nyc-taxi-ingest-<XX> -streamRegion us-east-1
⋅⋅* 7C: temporarily on the store using Athena View
        7CA: set Athena result destination to: nyc-taxi-store-7c-<XX>
        7CB: run a simple query to validate records are being properly read: SELECT * FROM nyc-taxi-table-<XX> WHERE amount < 5 
        7CC: store this query as a View for reuse later on and run it
⋅⋅* 7D: permanently on the store using Glue Studio -> S3 to S3 -> Transform component -> Filter -> < 5USD -> keep partitioning
        7DA: navigate to Glue Studio and create a new visual job called nyc-taxi-transform-7d-<XX>
        7DB: select a S3 to S3 transform and use input bucket: nyc-taxi-store-<XX> and output nyc-taxi-store-7d-<XX>
        7DC: change Apply Mapping type to Transform - Filter
        7DD: set Job Details section with the role nyc-taxi-role-<XX> and a number of retries to the value of 1
        7DE: run the glue job
### Visualize the data through QuickSight
⋅⋅* 8A: navigate to the quicksight console and register standard edition of quicksight
⋅⋅* 8B: allow quicksight access into S3
⋅⋅*  8C: model a dashboard showing all trip destinations coloured by a number of passengers
### Control access through LakeFormation: we will skip this module, requires a follow-up with a specialist
### Convert pipeline 7B into CDK/CF Code:
⋅⋅* 10A: explore the CDK code provided and amend if needed
⋅⋅* 10B: run cdk synth to see CF Template generated from the code
⋅⋅* 10C: run cdk deploy to deploy infrastructure for 7B