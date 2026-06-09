locals {
  github_repo = "${var.github_owner}/${var.github_repository}"

  terraform_state_lock_key = "${var.terraform_state_key}.tflock"

  github_oidc_provider_url = "https://token.actions.githubusercontent.com"
}

resource "aws_iam_openid_connect_provider" "github" {
  url = local.github_oidc_provider_url

  client_id_list = [
    "sts.amazonaws.com",
  ]
}

data "aws_iam_policy_document" "github_actions_plan_assume_role" {
  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRoleWithWebIdentity",
    ]

    principals {
      type = "Federated"
      identifiers = [
        aws_iam_openid_connect_provider.github.arn,
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values = [
        "repo:${local.github_repo}:ref:refs/heads/main",
        "repo:${local.github_repo}:pull_request",
      ]
    }
  }
}

data "aws_iam_policy_document" "github_actions_apply_assume_role" {
  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRoleWithWebIdentity",
    ]

    principals {
      type = "Federated"
      identifiers = [
        aws_iam_openid_connect_provider.github.arn,
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"
      values = [
        "repo:${local.github_repo}:environment:dev",
        "repo:${local.github_repo}:ref:refs/heads/main",
      ]
    }
  }
}

data "aws_iam_policy_document" "terraform_plan" {
  statement {
    sid = "ReadTerraformStateBucket"

    actions = [
      "s3:ListBucket",
    ]

    resources = [
      "arn:aws:s3:::${var.terraform_state_bucket_name}",
    ]

    condition {
      test     = "StringLike"
      variable = "s3:prefix"
      values = [
        var.terraform_state_key,
        local.terraform_state_lock_key,
      ]
    }
  }

  statement {
    sid = "ReadTerraformStateObject"

    actions = [
      "s3:GetObject",
    ]

    resources = [
      "arn:aws:s3:::${var.terraform_state_bucket_name}/${var.terraform_state_key}",
    ]
  }

  statement {
    sid = "ManageTerraformStateLock"

    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
    ]

    resources = [
      "arn:aws:s3:::${var.terraform_state_bucket_name}/${local.terraform_state_lock_key}",
    ]
  }

  statement {
    sid = "ReadLakehouseBucketConfiguration"

    actions = [
      "s3:ListBucket",
      "s3:GetBucketLocation",
      "s3:GetBucketVersioning",
      "s3:GetBucketPublicAccessBlock",
      "s3:GetBucketOwnershipControls",
      "s3:GetEncryptionConfiguration",
      "s3:GetBucketTagging",
      "s3:GetBucketPolicy",
      "s3:GetBucketAcl",
      "s3:GetBucketCORS",
      "s3:GetBucketWebsite",
      "s3:GetBucketLogging",
      "s3:GetBucketRequestPayment",
      "s3:GetReplicationConfiguration",
      "s3:GetLifecycleConfiguration",
      "s3:GetAccelerateConfiguration",
      "s3:GetBucketObjectLockConfiguration",
    ]

    resources = [
      "arn:aws:s3:::${var.lakehouse_bucket_name}",
    ]
  }


  statement {
    sid = "ReadGitHubActionsOidcProvider"

    actions = [
      "iam:GetOpenIDConnectProvider",
    ]

    resources = [
      aws_iam_openid_connect_provider.github.arn,
    ]
  }

  statement {
    sid = "ReadGitHubActionsTerraformPlanRole"

    actions = [
      "iam:GetRole",
      "iam:GetRolePolicy",
      "iam:ListRolePolicies",
      "iam:ListAttachedRolePolicies",
    ]

    resources = [
      "arn:aws:iam::${var.aws_account_id}:role/${var.plan_role_name}",
      "arn:aws:iam::${var.aws_account_id}:role/${var.apply_role_name}",
    ]
  }

  statement {
    sid = "ReadDatabricksStorageIamResources"

    actions = [
      "iam:GetRole",
      "iam:GetRolePolicy",
      "iam:ListRolePolicies",
      "iam:ListAttachedRolePolicies",
      "iam:GetInstanceProfile",
    ]

    resources = [
      "arn:aws:iam::${var.aws_account_id}:role/${var.storage_access_role_name}",
      "arn:aws:iam::${var.aws_account_id}:instance-profile/${var.storage_access_instance_profile_name}",
    ]
  }
}

data "aws_iam_policy_document" "terraform_apply" {
  source_policy_documents = [
    data.aws_iam_policy_document.terraform_plan.json,
  ]

  statement {
    sid = "WriteTerraformStateObject"

    actions = [
      "s3:GetObject",
      "s3:PutObject",
    ]

    resources = [
      "arn:aws:s3:::${var.terraform_state_bucket_name}/${var.terraform_state_key}",
    ]
  }

  statement {
    sid = "ManageLakehouseBucketConfiguration"

    actions = [
      "s3:PutBucketVersioning",
      "s3:PutBucketPublicAccessBlock",
      "s3:PutBucketOwnershipControls",
      "s3:PutEncryptionConfiguration",
      "s3:PutBucketTagging",
      "s3:PutLifecycleConfiguration",
      "s3:DeleteLifecycleConfiguration",
    ]

    resources = [
      "arn:aws:s3:::${var.lakehouse_bucket_name}",
    ]
  }

  statement {
    sid = "ManageGitHubActionsOidcProvider"

    actions = [
      "iam:GetOpenIDConnectProvider",
      "iam:CreateOpenIDConnectProvider",
      "iam:DeleteOpenIDConnectProvider",
      "iam:UpdateOpenIDConnectProviderThumbprint",
      "iam:AddClientIDToOpenIDConnectProvider",
      "iam:RemoveClientIDFromOpenIDConnectProvider",
    ]

    resources = [
      aws_iam_openid_connect_provider.github.arn,
    ]
  }

  statement {
    sid = "ManageTerraformCicdRoles"

    actions = [
      "iam:GetRole",
      "iam:CreateRole",
      "iam:DeleteRole",
      "iam:UpdateAssumeRolePolicy",
      "iam:GetRolePolicy",
      "iam:PutRolePolicy",
      "iam:DeleteRolePolicy",
      "iam:ListRolePolicies",
      "iam:ListAttachedRolePolicies",
      "iam:TagRole",
      "iam:UntagRole",
    ]

    resources = [
      "arn:aws:iam::${var.aws_account_id}:role/${var.plan_role_name}",
      "arn:aws:iam::${var.aws_account_id}:role/${var.apply_role_name}",
    ]
  }

  statement {
    sid = "ManageDatabricksStorageIamResources"

    actions = [
      "iam:GetRole",
      "iam:CreateRole",
      "iam:DeleteRole",
      "iam:UpdateAssumeRolePolicy",
      "iam:GetRolePolicy",
      "iam:PutRolePolicy",
      "iam:DeleteRolePolicy",
      "iam:ListRolePolicies",
      "iam:ListAttachedRolePolicies",
      "iam:GetInstanceProfile",
      "iam:CreateInstanceProfile",
      "iam:DeleteInstanceProfile",
      "iam:AddRoleToInstanceProfile",
      "iam:RemoveRoleFromInstanceProfile",
      "iam:TagRole",
      "iam:UntagRole",
      "iam:TagInstanceProfile",
      "iam:UntagInstanceProfile",
    ]

    resources = [
      "arn:aws:iam::${var.aws_account_id}:role/${var.storage_access_role_name}",
      "arn:aws:iam::${var.aws_account_id}:instance-profile/${var.storage_access_instance_profile_name}",
    ]
  }
}

resource "aws_iam_role" "terraform_plan" {
  name               = var.plan_role_name
  assume_role_policy = data.aws_iam_policy_document.github_actions_plan_assume_role.json
}

resource "aws_iam_role_policy" "terraform_plan" {
  name   = "${var.plan_role_name}-policy"
  role   = aws_iam_role.terraform_plan.id
  policy = data.aws_iam_policy_document.terraform_plan.json
}

resource "aws_iam_role" "terraform_apply" {
  name               = var.apply_role_name
  assume_role_policy = data.aws_iam_policy_document.github_actions_apply_assume_role.json
}

resource "aws_iam_role_policy" "terraform_apply" {
  name   = "${var.apply_role_name}-policy"
  role   = aws_iam_role.terraform_apply.id
  policy = data.aws_iam_policy_document.terraform_apply.json
}

