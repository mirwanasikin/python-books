# Day 14 — Week 2 Project

Keywords: All from Week 2 (`def, return, lambda, global, nonlocal, try, except, finally, raise, assert, with, import, from, as, del, split, join, replace, strip, open, read, write, close`)

## Project: log_analyzer.py

Build a log analyzer that parses nginx access logs and extracts key statistics using all concepts from Week 2.

### Project Specification

**Objective**: Create a log analyzer that processes nginx access logs and generates comprehensive statistics about requests, status codes, IP addresses, and endpoints.

**Input**: Nginx access log file (typical format: `$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"`)

**Output**: Structured statistics including:
1. Request count by HTTP method
2. Status code distribution
3. Top requesting IP addresses
4. Most requested endpoints
5. User agent distribution
6. Error rate calculation
7. Peak request times

### Starter Code
```python
#!/usr/bin/env python3
"""
Nginx Log Analyzer
Parses nginx access logs and generates comprehensive statistics
"""

import re
import json
import sys
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from pathlib import Path

def validate_log_file(file_path):
    """Validate that log file exists and is readable"""
    try:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Log file {file_path} does not exist")
        if not path.is_file():
            raise ValueError(f"{file_path} is not a file")
        if not os.access(file_path, os.R_OK):
            raise PermissionError(f"No read permission for {file_path}")
        
        return True
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        return False

def parse_log_line(line):
    """Parse a single log line using regex pattern"""
    # Common nginx log format
    log_pattern = re.compile(
        r'(?P<ip>\\d+\\.\\d+\\.\\d+\\.\\d+) '           # Remote IP
        r'- (?P<user>\\S+) '                        # Remote user
        r'\\[(?P<time>.+?)\\] '                      # Time
        r'"(?P<request>.+?)\" '                     # Request
        r'(?P<status>\\d{3}) '                       # Status code
        r'(?P<size>\\d+) '                            # Body bytes sent
        r'"(?P<referer>.+?)\" '                       # Referer
        r'"(?P<agent>.+?)"'                         # User agent
    )
    
    match = log_pattern.match(line)
    return match.groupdict() if match else None

def extract_endpoint(request):
    """Extract HTTP method and endpoint from request string"""
    parts = request.split()
    if len(parts) >= 2:
        return parts[0], parts[1]
    return None, None

def analyze_log_file(file_path):
    """Analyze log file and generate statistics"""
    stats = {
        'total_requests': 0,
        'method_counts': Counter(),
        'status_counts': Counter(),
        'ip_counts': Counter(),
        'endpoint_counts': Counter(),
        'agent_counts': Counter(),
        'errors': [],
        'request_times': []
    }
    
    try:
        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                # Parse log line
                parsed = parse_log_line(line)
                if not parsed:
                    stats['errors'].append(f"Line {line_num}: Failed to parse")
                    continue
                
                # Extract data
                stats['total_requests'] += 1
                stats['method_counts'][parsed['request'].split()[0]] += 1
                stats['status_counts'][parsed['status']] += 1
                stats['ip_counts'][parsed['ip']] += 1
                stats['agent_counts'][parsed['agent']] += 1
                
                # Extract and count endpoint
                method, endpoint = extract_endpoint(parsed['request'])
                if endpoint:
                    stats['endpoint_counts'][endpoint] += 1
                
                # Parse timestamp
                try:
                    time_str = parsed['time']
                    # Remove timezone info for simplicity
                    time_str = time_str.split()[0] + ' ' + time_str.split()[1]
                    log_time = datetime.strptime(time_str, '%d/%b/%Y:%H:%M:%S %z')
                    stats['request_times'].append(log_time)
                except Exception:
                    stats['errors'].append(f"Line {line_num}: Invalid time format")
    
    except Exception as e:
        print(f"✗ Error reading log file: {e}")
        return None
    
    return stats

def generate_report(stats):
    """Generate human-readable report from statistics"""
    if not stats or stats['total_requests'] == 0:
        return "No data to analyze"
    
    report = "Nginx Log Analysis Report\n"
    report += "=" * 60 + "\n\n"
    
    # Request count
    report += f"Total Requests: {stats['total_requests']}\n"
    report += f"Error Rate: {(len(stats['errors']) / stats['total_requests'] * 100):.2f}%\n\n"
    
    # Status codes
    report += "Status Code Distribution:\n"
    for status, count in sorted(stats['status_counts'].items()):
        percentage = (count / stats['total_requests'] * 100)
        report += f"  {status}: {count} ({percentage:.1f}%)\n"
    report += "\n"
    
    # Top IPs
    report += "Top Requesting IP Addresses:\n"
    for ip, count in stats['ip_counts'].most_common(5):
        report += f"  {ip}: {count} requests\n"
    report += "\n"
    
    # Top endpoints
    report += "Most Requested Endpoints:\n"
    for endpoint, count in stats['endpoint_counts'].most_common(5):
        report += f"  {endpoint}: {count} requests\n"
    report += "\n"
    
    # Error details
    if stats['errors']:
        report += "Parsing Errors:\n"
        for error in stats['errors'][:5]:
            report += f"  {error}\n"
        if len(stats['errors']) > 5:
            report += f"  ... and {len(stats['errors']) - 5} more\n"
    
    return report

def save_json_report(stats, output_path='/tmp/log_analysis.json'):
    """Save analysis results as JSON"""
    try:
        # Convert Counter objects to dict for JSON serialization
        json_stats = {
            'total_requests': stats['total_requests'],
            'method_counts': dict(stats['method_counts']),
            'status_counts': dict(stats['status_counts']),
            'ip_counts': dict(stats['ip_counts']),
            'endpoint_counts': dict(stats['endpoint_counts']),
            'agent_counts': dict(stats['agent_counts']),
            'error_count': len(stats['errors'])
        }
        
        with open(output_path, 'w') as f:
            json.dump(json_stats, f, indent=2, default=str)
        
        print(f"✓ JSON report saved to {output_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to save JSON report: {e}")
        return False

def main(log_file_path):
    """Main execution function"""
    print("=" * 60)
    print("Nginx Log Analyzer - Week 2 Project")
    print("=" * 60)
    print()
    
    # Validate input
    if not validate_log_file(log_file_path):
        return 1
    
    print(f"Analyzing log file: {log_file_path}")
    
    # Analyze log file
    stats = analyze_log_file(log_file_path)
    if not stats:
        print("Failed to analyze log file")
        return 1
    
    # Generate and display report
    report = generate_report(stats)
    print(report)
    
    # Save JSON report
    save_json_report(stats)
    
    print()
    print("=" * 60)
    print("Analysis completed successfully!")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python log_analyzer.py <log_file_path>")
        print("Example: python log_analyzer.py /var/log/nginx/access.log")
        sys.exit(1)
    
    log_path = sys.argv[1]
    exit_code = main(log_path)
    sys.exit(exit_code)
```\n\n### Tasks\n\n1. **Read + type every example** in the starter code above\n2. **Implement missing functions**: Add implementations for `check_service_status`, `log_service_status`, `send_alert`, etc.\n3. **Add error handling** for all file operations and parsing failures\n4. **Add command-line argument validation**\n5. **Implement comprehensive test suite** for all functions\n6. **Test the script** on a sample log file\n7. **Create sample log files** for testing\n\n### Success Criteria\n\n- [ ] Script runs without errors on Linux\n- [ ] All functions handle errors gracefully\n- [ ] Output is clearly formatted and human-readable\n- [ ] JSON report is generated successfully\n- [ ] Comprehensive test coverage with pytest\n- [ ] Uses all Week 2 concepts: functions, scope, error handling, context managers, modules, strings, regex, file I/O\n- [ ] Proper exception handling for all edge cases\n- [ ] Command-line interface works as expected\n\n### DevOps Context\n\nThis log analyzer represents a common DevOps task:\n\n- **Monitoring**: Extract and analyze server logs for operational insights\n- **Debugging**: Quickly identify issues from log statistics\n- **Capacity Planning**: Analyze traffic patterns and endpoint usage\n- **Security**: Detect abnormal request patterns or error rates\n- **Automation**: Integrate with monitoring systems and alerting\n\n**Real-world applications**:\n\n1. **Performance Monitoring**: Track response times and status code distributions\n2. **Security Auditing**: Analyze request patterns and detect potential attacks\n3. **Capacity Planning**: Identify peak usage times and trending endpoints\n4. **Troubleshooting**: Quickly locate problematic requests or error spikes\n5. **Compliance**: Generate reports for audit requirements\n\n**Integration with DevOps toolchain**:\n\n```python\n# Integration with monitoring systems\nfrom automation.monitoring import setup_monitoring\nfrom automation.alerts import send_alert\n\ndef process_analysis_results(stats):\n    \"\"\"Process analysis results and trigger alerts if needed\"\"\"\n    error_rate = len(stats.get('errors', [])) / stats.get('total_requests', 1)\n    \n    if error_rate > 0.05:  # 5% error threshold\n        send_alert(f\"High error rate detected: {error_rate:.2%}\")\n    \n    top_endpoint, top_count = stats['endpoint_counts'].most_common(1)[0]\n    if top_count > stats['total_requests'] * 0.3:  # 30% on single endpoint\n        send_alert(f\"Single endpoint consuming {top_count/stats['total_requests']:.1%} of traffic\")\n\n# Schedule regular analysis via cron\n# 0 */6 * * * /usr/bin/python /opt/automation/log_analyzer.py /var/log/nginx/access.log >> /var/log/analysis.log 2>&1\n```\n\n## Todo\n- [ ] Read + type every example\n- [ ] Complete exercises (no copy-paste)\n- [ ] Pass `pytest tests/day14 -v`\n- [ ] Build mini-script for Linux\n\n## Test\nRun: `pytest tests/day14 -v` — see `tests/day14/test_day14.py`\n", "filePath": "/home/irwan/book_md/book/02-week2-functions-system/day14-week2-project.md"}