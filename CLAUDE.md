# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A starter kit for the Scripps Research 2026 Computational Biology & Bioinformatics Hackathon (May 29 – June 1). It gives participants a pre-configured Claude Code environment with specialized skills for AWS and HPC access.

## Key Commands

**AWS smoke test** (validates CLI install, SSO login, S3 round-trip, EC2 launch/terminate, Bedrock access):
```bash
bash test_skill.sh
```

**AWS SSO login** (required before any AWS operations):
```bash
aws sso login --profile hackathon
```

**Run the Bedrock/AWS validation script** (requires boto3):
```bash
python hello-world/hello_aws.py
```

**Submit the example Slurm job** (on Garibaldi HPC, not locally):
```bash
sbatch hello-world/hello_hpc.slurm
```

## Architecture

**Claude Code integration** is the core of this project — not a traditional app. Key extension points:

- `.claude/commands/hackathon-aws.md` — the `/hackathon-aws` slash command. It is gated: it only activates if the AWS MCP servers (`mcp__aws_*` or `mcp__s3_*`) are present in context. Contains the full VPC/networking inventory, EC2 launch templates, S3 patterns, and Bedrock model inference profile IDs for the shared AWS account (`127696279288`, `us-west-2`).
- `.claude/skills/scripps-garibaldi-hpc/SKILL.md` — auto-loaded HPC skill. Triggers when the user asks about Garibaldi, Slurm, or the HPC cluster. Contains cluster-specific Slurm templates for interactive sessions, batch jobs, GPU jobs, array jobs, and parallel jobs.

**AWS infrastructure** (all pre-provisioned in the shared account):
- Private VPC with NAT gateway and S3 gateway endpoint
- EICE (EC2 Instance Connect Endpoint) for SSH to private instances without a bastion host
- EC2 launch templates with instance profiles granting S3 + Bedrock access
- Amazon Bedrock with inference profiles for Claude Haiku 4.5, Sonnet 4.5/4.6, and Opus 4.7

**Shared data**: `s3://scripps-hackathon-2026/` (read-only, requester-pays disabled). Personal buckets should be named `hackathon-<yourname>-<purpose>` in `us-west-2`.

## HPC Notes

- Login hosts: `garibaldi.scripps.edu` or `login02.scripps.edu`
- Never run compute jobs on the login node — use `srun` (interactive) or `sbatch` (batch)
- Always `module purge` before `module load` in job scripts
- Request an account by emailing hpc@scripps.edu if you don't have one

## Bedrock Model IDs

When writing code that calls Bedrock via the inference profile ARNs:
- Haiku 4.5: `us.anthropic.claude-haiku-4-5-20251001-v1:0`
- Sonnet 4.5: `us.anthropic.claude-sonnet-4-5-20251001-v1:0`
- Sonnet 4.6: `us.anthropic.claude-sonnet-4-6-20251001-v1:0`
- Opus 4.7: `us.anthropic.claude-opus-4-7-20251001-v1:0`
