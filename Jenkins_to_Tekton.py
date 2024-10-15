import re
from collections import defaultdict
from datetime import datetime

def parse_jenkinsfile(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    pipeline_structure = defaultdict(list)
    build_steps = defaultdict(int)
    triggers = defaultdict(int)
    current_stage = None
    in_step = False

    stage_pattern = re.compile(r'^\s*stage\s*\(\s*["\']([^"\']+)["\']\s*\)\s*{')
    step_pattern = re.compile(r'^\s*steps\s*{')
    plugin_pattern = re.compile(r'^\s*([a-zA-Z0-9]+)\s*\(')
    trigger_pattern = re.compile(r'^\s*(cron|pollSCM)\s*\(.*\)')

    for line in lines:
        # Detecting stages
        stage_match = stage_pattern.search(line)
        if stage_match:
            current_stage = stage_match.group(1)
            pipeline_structure[current_stage] = []
            in_step = False

        # Detecting steps block within stages
        if step_pattern.search(line):
            in_step = True

        # Extracting steps and counting their usage
        if in_step and current_stage:
            plugin_match = plugin_pattern.search(line)
            if plugin_match:
                plugin_name = plugin_match.group(1)
                pipeline_structure[current_stage].append(plugin_name)
                build_steps[plugin_name] += 1

        # Extracting triggers and counting their usage
        trigger_match = trigger_pattern.search(line)
        if trigger_match:
            trigger_name = trigger_match.group(1)
            triggers[trigger_name] += 1

    return pipeline_structure, build_steps, triggers


# Function to generate an audit summary
def generate_audit_summary(parsed_pipeline, build_steps, triggers):
    total_pipelines = len(parsed_pipeline)
    total_build_steps = sum(build_steps.values())
    total_triggers = sum(triggers.values())

    # Sorting build steps and triggers by frequency of use
    sorted_build_steps = sorted(build_steps.items(), key=lambda x: x[1], reverse=True)
    sorted_triggers = sorted(triggers.items(), key=lambda x: x[1], reverse=True)

    # Creating the summary
    audit_summary = f"Audit Summary\n{'-'*20}\n"
    audit_summary += f"Performed at : {datetime.now().strftime('%d/%m/%y %H:%M')}\n\n"
    
    # Pipeline summary
    audit_summary += f"Pipelines\nTotal : {total_pipelines}\n\n"

    # Build steps summary
    audit_summary += f"Build Steps\nTotal : {total_build_steps}\n"
    for step, count in sorted_build_steps:
        audit_summary += f"-> {step} : {count}\n"
    
    # Trigger summary
    audit_summary += f"\nTriggers\nTotal : {total_triggers}\n"
    for trigger, count in sorted_triggers:
        audit_summary += f"-> {trigger} : {count}\n"
    
    return audit_summary


def audit_jenkinsfile(jenkinsfile_path):
    parsed_pipeline, build_steps, triggers = parse_jenkinsfile(jenkinsfile_path)
    audit_summary = generate_audit_summary(parsed_pipeline, build_steps, triggers)
    
    print(audit_summary)


jenkinsfile_path = 'Jenkinsfile'
audit_jenkinsfile(jenkinsfile_path)