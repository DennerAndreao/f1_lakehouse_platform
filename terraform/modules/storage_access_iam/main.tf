data "aws_iam_policy_document" "assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type = "AWS"
      identifiers = [
        "arn:aws:iam::${var.account_id}:role/${var.role_name}",
        "arn:aws:iam::414351767826:role/unity-catalog-prod-UCMasterRole-14S5ZJVKOTYTL",
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "sts:ExternalId"
      values   = [var.external_id]
    }
  }
}

data "aws_iam_policy_document" "lakehouse_access" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
      "s3:ListBucket",
      "s3:GetBucketLocation",
      "s3:GetLifecycleConfiguration",
      "s3:PutLifecycleConfiguration",
    ]

    resources = [
      "${var.lakehouse_bucket_arn}/*",
      var.lakehouse_bucket_arn,
    ]
  }

  statement {
    actions = ["sts:AssumeRole"]

    resources = [
      "arn:aws:iam::${var.account_id}:role/${var.role_name}",
    ]
  }

  statement {
    sid = "ManagedFileEventsSetupStatement"

    actions = [
      "s3:GetBucketNotification",
      "s3:PutBucketNotification",
      "sns:ListSubscriptionsByTopic",
      "sns:GetTopicAttributes",
      "sns:SetTopicAttributes",
      "sns:CreateTopic",
      "sns:TagResource",
      "sns:Publish",
      "sns:Subscribe",
      "sqs:CreateQueue",
      "sqs:DeleteMessage",
      "sqs:ReceiveMessage",
      "sqs:SendMessage",
      "sqs:GetQueueUrl",
      "sqs:GetQueueAttributes",
      "sqs:SetQueueAttributes",
      "sqs:TagQueue",
      "sqs:ChangeMessageVisibility",
      "sqs:PurgeQueue",
    ]

    resources = [
      var.lakehouse_bucket_arn,
      "arn:aws:sqs:*:${var.account_id}:csms-*",
      "arn:aws:sns:*:${var.account_id}:csms-*",
    ]
  }

  statement {
    sid = "ManagedFileEventsListStatement"

    actions = [
      "sqs:ListQueues",
      "sqs:ListQueueTags",
      "sns:ListTopics",
    ]

    resources = [
      "arn:aws:sqs:*:${var.account_id}:csms-*",
      "arn:aws:sns:*:${var.account_id}:csms-*",
    ]
  }

  statement {
    sid = "ManagedFileEventsTeardownStatement"

    actions = [
      "sns:Unsubscribe",
      "sns:DeleteTopic",
      "sqs:DeleteQueue",
    ]

    resources = [
      "arn:aws:sqs:*:${var.account_id}:csms-*",
      "arn:aws:sns:*:${var.account_id}:csms-*",
    ]
  }
}

resource "aws_iam_role" "storage_access" {
  name               = var.role_name
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role_policy" "lakehouse_access" {
  name   = var.inline_policy_name
  role   = aws_iam_role.storage_access.id
  policy = data.aws_iam_policy_document.lakehouse_access.json
}

resource "aws_iam_instance_profile" "storage_access" {
  name = var.instance_profile_name
  role = aws_iam_role.storage_access.name
}
