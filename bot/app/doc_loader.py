def load_fest_documents(txt_path: str):
    """
    Load festival info from txt file with semantic section parsing.
    Uses ### SECTION: markers for proper chunking.
    """
    try:
        print(f"📖 Loading festivals from: {txt_path}")
        
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        sections = []
        max_sections = 12  # Allow more sections since they're well-defined
        
        # Split on section markers: ### SECTION: NAME ###
        raw_sections = content.split('### SECTION:')
        
        for section in raw_sections:
            section = section.strip()
            if not section or len(section) < 30:
                continue
            
            # Remove the closing ### if present
            if section.startswith('###'):
                section = section[3:].strip()
            if '###' in section:
                # Extract section name and content
                parts = section.split('###', 1)
                if len(parts) == 2:
                    section_name = parts[0].strip()
                    section_content = parts[1].strip()
                    # Combine for better context
                    full_section = f"{section_name}: {section_content}"
                else:
                    full_section = section
            else:
                full_section = section
            
            # Keep sections reasonably sized (up to 600 chars for better context)
            if len(full_section) > 600:
                full_section = full_section[:600]
            
            sections.append(full_section)
            
            if len(sections) >= max_sections:
                break
        
        print(f"   ✅ Loaded {len(sections)} festival sections")
        if sections:
            print(f"   Sample: {sections[0][:100]}...")
        
        return sections
        
    except Exception as e:
        print(f"❌ Error loading festivals: {e}")
        return []
