# Jenkinsfile Audit Tool
This Python script analyzes Jenkinsfiles to provide an audit summary of their structure, build steps, and triggers. It's designed to help DevOps engineers and developers understand the composition of their Jenkins pipelines across projects.
- Parses Jenkinsfile syntax to extract stages, steps, and triggers
- Provides a summary of total pipelines (stages), build steps, and triggers
- Counts and sorts build steps by frequency of use
- Identifies and counts trigger types (e.g., pollSCM, cron)
- Generates a human-readable audit summary
