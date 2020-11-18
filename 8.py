from aws_cdk import (

    aws_iam as iam,

    aws_s3 as s3,

    aws_lambda as _lambda,

    aws_kinesis as kinesis,

    aws_kinesisfirehose as kinesisfirehose,

    core

)





class DemoPythonSampleStack(core.Stack):



    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:

        super().__init__(scope, id, **kwargs)



        bucket = s3.Bucket(

            self, "Bucket",

            bucket_name = "nyc-taxi-under5-miro-src-20201118"

        )



        #stream = kinesis.Stream(

        #    self, "Stream",

        #    stream_name = "nyc-taxi-replay-miro"

        #)

        stream = kinesis.Stream.from_stream_arn(

            self, "ExistingStream", 

            #stream_arn = "arn:aws:kinesis:::stream/nyc-taxi-replay-miro"

            stream_arn = "arn:aws:kinesis:us-west-2:711127748486:stream/nyc-taxi-replay-miro"

        )



        deliverystreamrole = iam.Role(

            self, "DeliveryStreamRole",

            assumed_by = iam.ServicePrincipal("firehose.amazonaws.com")

        )



        deliverystreamrole.add_to_policy(iam.PolicyStatement(

            effect=iam.Effect.ALLOW,

            resources=[bucket.bucket_arn, bucket.arn_for_objects("*")],

            actions=[

                "s3:AbortMultipartUpload",

                "s3:GetBucketLocation",

                "s3:GetObject",

                "s3:ListBucket",

                "s3:ListBucketMultipartUploads",

                "s3:PutObject"

            ]

        ))



        deliverystreamrole.add_to_policy(iam.PolicyStatement(

            effect=iam.Effect.ALLOW,

            resources=[

                #stream.stream_arn

                "arn:aws:kinesis:*:*:stream/nyc-taxi-replay-miro"

            ],

            actions=[

                "kinesis:DescribeStream",

                "kinesis:GetShardIterator",

                "kinesis:GetRecords",

                "kinesis:ListShards"

            ]

        ))



        deliverystreamrole.add_to_policy(iam.PolicyStatement(

            effect=iam.Effect.ALLOW,

            resources=[

                "arn:aws:logs:*:*:*"

            ],

            actions=[

                "logs:*"

            ]

        ))



        lambdafunctionrole = iam.Role(

            self, "LambdaFunctionRole",

            assumed_by = iam.ServicePrincipal("lambda.amazonaws.com")

        )

        

        lambdafunctionrole.add_to_policy(iam.PolicyStatement(

            effect=iam.Effect.ALLOW,

            resources=["arn:aws:logs:*:*:*"],

            actions=[

                "logs:*"

            ]

        ))



        lambdafunctioncode = "\n"\

            "from __future__ import print_function\n"\

            "import base64\n"\

            "print('Loading function')\n"\

            "def lambda_handler(event, context):\n"\

            "    output = []\n"\

            "    for record in event['records']:\n"\

            "        print(record['recordId'])\n"\

            "        payload = base64.b64decode(record['data'])\n"\

            "        # Do custom processing on the payload here\n"\

            "        output_record = {\n"\

            "            'recordId': record['recordId'],\n"\

            "            'result': 'Ok',\n"\

            "            'data': base64.b64encode(payload)\n"\

            "        }\n"\

            "        output.append(output_record)\n"\

            "    print('Successfully processed {} records.'.format(len(event['records'])))\n"\

            "    return {'records': output}\n"\

            "\n"



        function = _lambda.Function(

            self, "LambdaFunction",

            runtime = _lambda.Runtime.PYTHON_2_7,

            handler = "index.lambda_handler",

            code = _lambda.Code.from_inline(lambdafunctioncode),

            role = lambdafunctionrole,

            timeout = core.Duration.seconds(60),

            memory_size = 128

        )



        deliverystreamrole.add_to_policy(iam.PolicyStatement(

            effect=iam.Effect.ALLOW,

            resources=[function.function_arn],

            actions=[

                "lambda:InvokeFunction",

                "lambda:GetFunctionConfiguration"

            ]

        ))



        #deliverystream = kinesisfirehose.CfnDeliveryStream(

        #    self, "DeliveryStream",

        #    delivery_stream_name = "nyc-taxi-delivery-under5-miro",

        #    delivery_stream_type = "KinesisStreamAsSource",

        #    extended_s3_destination_configuration = kinesisfirehose.CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty(

        #        bucket_arn = bucket.bucket_arn, 

        #        role_arn = deliverystreamrole.role_arn, 

        #        processing_configuration = kinesisfirehose.CfnDeliveryStream.ProcessingConfigurationProperty(

        #            enabled = True,

        #            processors = [kinesisfirehose.CfnDeliveryStream.ProcessorProperty(

        #                type = "Lambda",

        #                parameters = [kinesisfirehose.CfnDeliveryStream.ProcessorParameterProperty(

        #                    parameter_name = "LambdaArn",

        #                    parameter_value = function.function_arn

        #                )]

        #            )]

        #        )

        #    ),

        #    kinesis_stream_source_configuration = kinesisfirehose.CfnDeliveryStream.KinesisStreamSourceConfigurationProperty(

        #        kinesis_stream_arn = stream.stream_arn, 

        #        role_arn = deliverystreamrole.role_arn

        #    )

        #)

