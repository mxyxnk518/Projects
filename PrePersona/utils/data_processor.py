import streamlit as st
import pandas as pd
import json
import os
import re
from datetime import datetime
from io import StringIO

def get_upload_types():
    """Return the available data types for upload."""
    return {
        "Text/Journal": ["txt", "md", "docx"],
        "Chat Export": ["txt", "json"],
        "Calendar": ["ics", "csv"],
        "Email": ["eml", "txt"],
        "Social Media Export": ["json", "csv"],
    }

def process_user_data(uploaded_files, user_name):
    """
    Process various types of user data from uploaded files.
    Returns processed data and a summary of what was extracted.
    """
    processed_data = []
    summary = {
        "total_entries": 0,
        "total_words": 0,
        "date_range": {"start": None, "end": None},
        "file_types_processed": {},
    }
    
    # Process each uploaded file
    for uploaded_file in uploaded_files:
        file_type = uploaded_file.name.split('.')[-1].lower()
        content = uploaded_file.read()
        
        # Convert bytes to string for text files
        if file_type in ["txt", "md", "json", "csv"]:
            try:
                content = content.decode("utf-8")
            except UnicodeDecodeError:
                st.error(f"Could not decode {uploaded_file.name}. It might not be a text file.")
                continue
                
        # Process based on file type
        if file_type == "txt":
            data_entries = process_text_file(content, uploaded_file.name, user_name)
        elif file_type == "json":
            data_entries = process_json_file(content, uploaded_file.name, user_name)
        elif file_type == "csv":
            data_entries = process_csv_file(content, uploaded_file.name, user_name)
        elif file_type == "md":
            data_entries = process_markdown_file(content, uploaded_file.name, user_name)
        else:
            st.warning(f"File type {file_type} is not fully supported yet. Basic processing applied.")
            data_entries = [{"text": f"Content from {uploaded_file.name}", "metadata": {"source": uploaded_file.name, "type": "unknown"}}]
        
        if data_entries:
            processed_data.extend(data_entries)
            
            # Update summary statistics
            summary["total_entries"] += len(data_entries)
            word_count = sum(len(entry["text"].split()) for entry in data_entries)
            summary["total_words"] += word_count
            
            # Track file types
            if file_type in summary["file_types_processed"]:
                summary["file_types_processed"][file_type] += 1
            else:
                summary["file_types_processed"][file_type] = 1
            
            # Update date range if timestamps are available
            dates = [entry["metadata"].get("timestamp") for entry in data_entries if "timestamp" in entry["metadata"]]
            valid_dates = [d for d in dates if d]
            if valid_dates:
                min_date = min(valid_dates)
                max_date = max(valid_dates)
                
                if not summary["date_range"]["start"] or min_date < summary["date_range"]["start"]:
                    summary["date_range"]["start"] = min_date
                
                if not summary["date_range"]["end"] or max_date > summary["date_range"]["end"]:
                    summary["date_range"]["end"] = max_date
    
    return processed_data, summary

def process_text_file(content, filename, user_name):
    """Process plain text files, attempting to identify journal entries or chat logs."""
    entries = []
    
    # Check if this is a chat log by looking for common patterns
    # Like "Person: Message" or "[Time] Person: Message"
    lines = content.split('\n')
    is_chat = False
    
    # Simple heuristic: if more than 25% of non-empty lines contain ": " pattern, it's likely a chat
    chat_lines = [line for line in lines if ": " in line]
    if len(chat_lines) > 0 and len(chat_lines) / len([l for l in lines if l.strip()]) > 0.25:
        is_chat = True
    
    if is_chat:
        # Process as chat
        current_message = {"sender": "", "message": "", "timestamp": None}
        
        for line in lines:
            # Try to match different chat formats
            chat_match = re.match(r'\[(.*?)\]\s*(.*?):\s*(.*)', line) or re.match(r'(.*?):\s*(.*)', line)
            
            if chat_match and len(chat_match.groups()) >= 2:
                # If we have a current message, add it before starting a new one
                if current_message["sender"] and current_message["message"]:
                    sender = current_message["sender"]
                    # Create personal perspective if the sender is the user
                    if sender.lower() in [user_name.lower(), "me", "myself", "i"]:
                        perspective = f"When asked about {current_message['message'][:50]}..., I said: {current_message['message']}"
                    else:
                        perspective = f"{sender} asked/said: {current_message['message']}, and this is relevant to how I communicate with others."
                    
                    entries.append({
                        "text": perspective,
                        "metadata": {
                            "source": filename,
                            "type": "chat",
                            "sender": sender,
                            "timestamp": current_message["timestamp"],
                            "original_text": current_message["message"]
                        }
                    })
                
                # Start a new message
                if len(chat_match.groups()) == 3:  # Has timestamp
                    timestamp_str, sender, message = chat_match.groups()
                    try:
                        timestamp = parse_timestamp(timestamp_str)
                    except:
                        timestamp = None
                else:  # No timestamp
                    sender, message = chat_match.groups()
                    timestamp = None
                
                current_message = {"sender": sender, "message": message, "timestamp": timestamp}
            elif current_message["sender"]:  # Continuation of previous message
                current_message["message"] += " " + line
        
        # Add the last message if it exists
        if current_message["sender"] and current_message["message"]:
            sender = current_message["sender"]
            if sender.lower() in [user_name.lower(), "me", "myself", "i"]:
                perspective = f"When discussing topics like '{current_message['message'][:50]}...', I said: {current_message['message']}"
            else:
                perspective = f"{sender} said: {current_message['message']}, and this is how I might process similar information."
            
            entries.append({
                "text": perspective,
                "metadata": {
                    "source": filename,
                    "type": "chat",
                    "sender": sender,
                    "timestamp": current_message["timestamp"],
                    "original_text": current_message["message"]
                }
            })
    else:
        # Process as journal or notes
        # Try to split into entries by looking for date patterns or clear separators
        potential_entries = re.split(r'\n\s*\n|\r\n\s*\r\n|(?=\d{1,2}[/-]\d{1,2}[/-]\d{2,4})|(?=\w+day,?\s+\w+\s+\d{1,2})', content)
        
        for entry_content in potential_entries:
            if not entry_content.strip():
                continue
                
            # Try to extract date if present
            date_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})|(\w+day,?\s+\w+\s+\d{1,2})', entry_content)
            timestamp = None
            
            if date_match:
                date_str = date_match.group(0)
                try:
                    timestamp = parse_timestamp(date_str)
                except:
                    pass  # If parsing fails, continue without a timestamp
            
            # Process the entry into a first-person perspective for better contextualization
            cleaned_entry = entry_content.strip()
            perspective_entry = f"In my personal notes, I wrote: {cleaned_entry}"
            
            entries.append({
                "text": perspective_entry,
                "metadata": {
                    "source": filename,
                    "type": "journal",
                    "timestamp": timestamp,
                    "original_text": cleaned_entry
                }
            })
    
    return entries

def process_json_file(content, filename, user_name):
    """Process JSON files which might be chat exports, social media data, etc."""
    entries = []
    
    try:
        data = json.loads(content)
        
        # Check if this is an array of messages or objects
        if isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    continue
                    
                # Try to identify what kind of item this is
                if "message" in item or "text" in item or "content" in item:
                    # Likely a message
                    message = item.get("message") or item.get("text") or item.get("content")
                    sender = item.get("sender") or item.get("author") or item.get("user") or "Unknown"
                    timestamp = None
                    
                    # Try different timestamp fields
                    for timestamp_field in ["timestamp", "date", "created_at", "time"]:
                        if timestamp_field in item:
                            try:
                                timestamp = parse_timestamp(str(item[timestamp_field]))
                                break
                            except:
                                pass
                    
                    # Create personal perspective
                    if sender.lower() in [user_name.lower(), "me", "myself", "i"]:
                        perspective = f"In a conversation, I wrote: {message}"
                    else:
                        perspective = f"{sender} wrote to me: {message}, and this is information I've processed."
                    
                    entries.append({
                        "text": perspective,
                        "metadata": {
                            "source": filename,
                            "type": "message",
                            "sender": sender,
                            "timestamp": timestamp,
                            "original_text": message
                        }
                    })
        # Check if this is a chat export with nested structure
        elif isinstance(data, dict):
            # Handle various JSON formats
            if "messages" in data and isinstance(data["messages"], list):
                # This might be a chat export
                for msg in data["messages"]:
                    if not isinstance(msg, dict):
                        continue
                        
                    message = msg.get("content") or msg.get("text") or msg.get("message", "")
                    sender = msg.get("sender") or msg.get("from") or "Unknown"
                    timestamp = None
                    
                    for ts_field in ["timestamp", "date", "time"]:
                        if ts_field in msg:
                            try:
                                timestamp = parse_timestamp(str(msg[ts_field]))
                                break
                            except:
                                pass
                    
                    if sender.lower() in [user_name.lower(), "me", "myself", "i"]:
                        perspective = f"I wrote in a conversation: {message}"
                    else:
                        perspective = f"In response to {sender} saying: '{message}', I would process this information."
                    
                    entries.append({
                        "text": perspective,
                        "metadata": {
                            "source": filename,
                            "type": "chat",
                            "sender": sender,
                            "timestamp": timestamp,
                            "original_text": message
                        }
                    })
    except json.JSONDecodeError:
        st.error(f"Could not parse {filename} as JSON.")
    
    return entries

def process_csv_file(content, filename, user_name):
    """Process CSV files which might be calendar data, exported messages, etc."""
    entries = []
    
    try:
        df = pd.read_csv(StringIO(content))
        
        # Try to determine what kind of CSV this is
        columns = df.columns.str.lower()
        
        # Check if this is a calendar/event export
        if any(col in columns for col in ["start", "end", "date", "event", "title", "subject"]):
            # Likely a calendar export
            for _, row in df.iterrows():
                event_title = None
                for title_col in ["title", "subject", "event", "summary"]:
                    if title_col in columns:
                        event_title = row[df.columns[columns == title_col][0]]
                        break
                
                if not event_title:
                    continue
                
                description = ""
                for desc_col in ["description", "notes", "details"]:
                    if desc_col in columns:
                        description = row[df.columns[columns == desc_col][0]]
                        break
                
                # Extract date
                timestamp = None
                for date_col in ["date", "start", "start date", "start_date"]:
                    if date_col in columns:
                        try:
                            date_val = row[df.columns[columns == date_col][0]]
                            timestamp = parse_timestamp(str(date_val))
                            break
                        except:
                            pass
                
                # Create contextual entry
                processed_text = f"I scheduled an event: {event_title}"
                if description and pd.notna(description):
                    processed_text += f" with details: {description}"
                if timestamp:
                    processed_text += f" on {timestamp.strftime('%Y-%m-%d')}"
                
                entries.append({
                    "text": processed_text,
                    "metadata": {
                        "source": filename,
                        "type": "calendar",
                        "timestamp": timestamp,
                        "original_text": f"{event_title} - {description}"
                    }
                })
        
        # Check if this is a message export
        elif any(col in columns for col in ["message", "text", "content", "sender", "from", "to"]):
            # Likely a message export
            for _, row in df.iterrows():
                message = None
                for msg_col in ["message", "text", "content"]:
                    if msg_col in columns:
                        message = row[df.columns[columns == msg_col][0]]
                        break
                
                if not message or pd.isna(message):
                    continue
                
                sender = "Unknown"
                for sender_col in ["sender", "from", "author", "user"]:
                    if sender_col in columns:
                        val = row[df.columns[columns == sender_col][0]]
                        if pd.notna(val):
                            sender = val
                            break
                
                timestamp = None
                for time_col in ["timestamp", "date", "time", "created_at"]:
                    if time_col in columns:
                        try:
                            time_val = row[df.columns[columns == time_col][0]]
                            if pd.notna(time_val):
                                timestamp = parse_timestamp(str(time_val))
                                break
                        except:
                            pass
                
                # Create personal perspective
                if str(sender).lower() in [user_name.lower(), "me", "myself", "i"]:
                    perspective = f"I wrote: {message}"
                else:
                    perspective = f"{sender} said to me: {message}, and I processed this information."
                
                entries.append({
                    "text": perspective,
                    "metadata": {
                        "source": filename,
                        "type": "message",
                        "sender": sender,
                        "timestamp": timestamp,
                        "original_text": str(message)
                    }
                })
    
    except Exception as e:
        st.error(f"Error processing CSV file {filename}: {str(e)}")
    
    return entries

def process_markdown_file(content, filename, user_name):
    """Process markdown files which might contain journal entries, notes, etc."""
    entries = []
    
    # Try to split the markdown into sections based on headers
    sections = re.split(r'^#{1,6}\s+', content, flags=re.MULTILINE)
    
    if len(sections) <= 1:
        # If no headers found, treat as a single entry
        entries.append({
            "text": f"In my notes, I wrote: {content.strip()}",
            "metadata": {
                "source": filename,
                "type": "notes",
                "timestamp": None,
                "original_text": content.strip()
            }
        })
    else:
        # Process each section
        headers = re.findall(r'^(#{1,6}\s+.+)$', content, flags=re.MULTILINE)
        
        for i, section_content in enumerate(sections[1:], 0):  # Skip the first split which is before any header
            header = headers[i] if i < len(headers) else "Untitled Section"
            
            # Try to extract date from header
            timestamp = None
            date_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})|(\w+day,?\s+\w+\s+\d{1,2})', header)
            if date_match:
                try:
                    timestamp = parse_timestamp(date_match.group(0))
                except:
                    pass
            
            # Process section content
            cleaned_section = section_content.strip()
            if not cleaned_section:
                continue
                
            # Create personal perspective
            perspective = f"In my notes titled '{header.strip('#').strip()}', I wrote: {cleaned_section}"
            
            entries.append({
                "text": perspective,
                "metadata": {
                    "source": filename,
                    "type": "notes",
                    "section": header.strip('#').strip(),
                    "timestamp": timestamp,
                    "original_text": cleaned_section
                }
            })
    
    return entries

def parse_timestamp(timestamp_str):
    """
    Try to parse a timestamp string into a datetime object.
    Handles various formats.
    """
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M",
        "%m/%d/%Y",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%b %d, %Y",
        "%B %d, %Y",
        "%a %b %d %H:%M:%S %Y",
        "%A, %B %d, %Y",
        "%A, %B %d"
    ]
    
    # For Unix timestamps
    if timestamp_str.isdigit():
        try:
            return datetime.fromtimestamp(int(timestamp_str))
        except:
            pass
    
    # Try different formats
    for fmt in formats:
        try:
            return datetime.strptime(timestamp_str, fmt)
        except ValueError:
            continue
    
    # If all parsing attempts fail
    raise ValueError(f"Could not parse timestamp: {timestamp_str}")
