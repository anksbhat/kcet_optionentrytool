"""
Updated parser to handle the complete 33 option entries from the user's data
"""
import pandas as pd
import os

def parse_user_provided_data():
    """Parse the 33 option entries provided by the user"""
    
    # Create the data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # The complete 33 option entries data provided by the user
    option_entries = [
        (1, "E009BW", "B TECH IN COMPUTER SCIENCE AND ENGINEERING", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "PES University 100 Feet Ring Road, Banashankari, 3rd Stage, Hosakerehalli, Near DSERT, , Bangalore KARNATAKA, pin code -560085"),
        (2, "E009AM", "B TECH IN COMPUTER SCIENCE & ENGINEERING (ARTIFICAL INTELLIGENCE & MACHINE LEARNING)", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "PES University 100 Feet Ring Road, Banashankari, 3rd Stage, Hosakerehalli, Near DSERT, , Bangalore KARNATAKA, pin code -560085"),
        (3, "E009BB", "B TECH IN ELECTRONICS & COMMUNICATION ENGINEERING", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "PES University 100 Feet Ring Road, Banashankari, 3rd Stage, Hosakerehalli, Near DSERT, , Bangalore KARNATAKA, pin code -560085"),
        (4, "E048AD", "ARTIFICIAL INTELLIGENCE AND DATA SCIENCE", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "B M S College of Engineering, Basavanagudi, Bangalore (AUTONOMOUS) POST BOX NO 1908, BULL TEMPLE ROAD,BANGALORE"),
        (5, "E048DS", "COMPUTER SCIENCE AND ENGINEERING(DATA SCIENCE)", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "B M S College of Engineering, Basavanagudi, Bangalore (AUTONOMOUS) POST BOX NO 1908, BULL TEMPLE ROAD,BANGALORE"),
        (6, "E048IC", "COMPUTER SCIENCE AND ENGG(INTERNET OF THINGS & CYBER SECURITY INCLUDING BLOCK CHAIN TECH)", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "B M S College of Engineering, Basavanagudi, Bangalore (AUTONOMOUS) POST BOX NO 1908, BULL TEMPLE ROAD,BANGALORE"),
        (7, "E048CB", "COMPUTER SCIENCE AND BUSINESS SYSTEMS", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "B M S College of Engineering, Basavanagudi, Bangalore (AUTONOMOUS) POST BOX NO 1908, BULL TEMPLE ROAD,BANGALORE"),
        (8, "E048EC", "ELECTRONICS AND COMMUNICATION ENGG", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "B M S College of Engineering, Basavanagudi, Bangalore (AUTONOMOUS) POST BOX NO 1908, BULL TEMPLE ROAD,BANGALORE"),
        (9, "E009BJ", "B TECH IN ELECTRICAL & ELECTRONICS ENGINEERING", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "PES University 100 Feet Ring Road, Banashankari, 3rd Stage, Hosakerehalli, Near DSERT, , Bangalore KARNATAKA, pin code -560085"),
        (10, "E005BT", "BIO-TECHNOLOGY", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "R. V. College of Engineering, Bangalore(AUTONOMOUS) R.V. VIDYANIKETAN POST, MYSORE ROAD,BANGALORE"),
        (11, "E005ME", "MECHANICAL ENGINEERING", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "R. V. College of Engineering, Bangalore(AUTONOMOUS) R.V. VIDYANIKETAN POST, MYSORE ROAD,BANGALORE"),
        (12, "E007DS", "COMPUTER SCIENCE AND ENGINEERING(DATA SCIENCE)", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "Dayananda Sagar College of Engineering, Bangalore(AUTONOMOUS) SHAVIGE MALLESHWARA HILLS, KUMARASWAMY LAYOUT, BANGALORE-560078"),
        (13, "E007AI", "ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "Dayananda Sagar College of Engineering, Bangalore(AUTONOMOUS) SHAVIGE MALLESHWARA HILLS, KUMARASWAMY LAYOUT, BANGALORE-560078"),
        (14, "E006SE", "AERO SPACE ENGINEERING", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "M S Ramaiah Institute of Technology, Bangalore(AUTONOMOUS) VIDYA SOUDHA,MSR NAGAR,MSRIT POST,BANGALORE - 560054."),
        (15, "E007CY", "COMPUTER SCIENCE AND ENGINEERING (CYBER SECURITY)", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "Dayananda Sagar College of Engineering, Bangalore(AUTONOMOUS) SHAVIGE MALLESHWARA HILLS, KUMARASWAMY LAYOUT, BANGALORE-560078"),
        (16, "E007IE", "INFORMATION SCIENCE AND ENGINEERING", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "Dayananda Sagar College of Engineering, Bangalore(AUTONOMOUS) SHAVIGE MALLESHWARA HILLS, KUMARASWAMY LAYOUT, BANGALORE-560078"),
        (17, "E007IC", "COMPUTER SCIENCE AND ENGG(INTERNET OF THINGS & CYBER SECURITY INCLUDING BLOCK CHAIN TECH)", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "Dayananda Sagar College of Engineering, Bangalore(AUTONOMOUS) SHAVIGE MALLESHWARA HILLS, KUMARASWAMY LAYOUT, BANGALORE-560078"),
        (18, "E007CD", "COMPUTER SCIENCE AND DESIGN", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "Dayananda Sagar College of Engineering, Bangalore(AUTONOMOUS) SHAVIGE MALLESHWARA HILLS, KUMARASWAMY LAYOUT, BANGALORE-560078"),
        (19, "E007EC", "ELECTRONICS AND COMMUNICATION ENGG", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "Dayananda Sagar College of Engineering, Bangalore(AUTONOMOUS) SHAVIGE MALLESHWARA HILLS, KUMARASWAMY LAYOUT, BANGALORE-560078"),
        (20, "E009BO", "B TECH IN BIO-TECHNOLOGY", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "PES University 100 Feet Ring Road, Banashankari, 3rd Stage, Hosakerehalli, Near DSERT, , Bangalore KARNATAKA, pin code -560085"),
        (21, "E006BT", "BIO-TECHNOLOGY", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "M S Ramaiah Institute of Technology, Bangalore(AUTONOMOUS) VIDYA SOUDHA,MSR NAGAR,MSRIT POST,BANGALORE - 560054."),
        (22, "E048BT", "BIO-TECHNOLOGY", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "B M S College of Engineering, Basavanagudi, Bangalore (AUTONOMOUS) POST BOX NO 1908, BULL TEMPLE ROAD,BANGALORE"),
        (23, "E007AE", "AERONAUTICAL ENGINEERING", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "Dayananda Sagar College of Engineering, Bangalore(AUTONOMOUS) SHAVIGE MALLESHWARA HILLS, KUMARASWAMY LAYOUT, BANGALORE-560078"),
        (24, "E126CB", "COMPUTER SCIENCE AND BUSINESS SYSTEMS", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "B M S Institute of Technology & Management, Yelahanka, Bangalore(AUTONOMOUS) POST BOX NO.6443, AVALAHALLI,DODDABALLAPURA MAIN ROAD,YELAHANKA, BANGALORE - 560064."),
        (25, "E007BT", "BIO-TECHNOLOGY", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "Dayananda Sagar College of Engineering, Bangalore(AUTONOMOUS) SHAVIGE MALLESHWARA HILLS, KUMARASWAMY LAYOUT, BANGALORE-560078"),
        (26, "E060AI", "ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "Dr. Ambedkar Institute of Technology, Bangalore(AUTONOMOUS) OUTER RING ROAD,NEAR JNANA BHARATHI CAMPUS,MALLATHAHALLI,BANGALORE-560056"),
        (27, "E006MD", "MEDICAL ELECTRONICS ENGINEERING", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "M S Ramaiah Institute of Technology, Bangalore(AUTONOMOUS) VIDYA SOUDHA,MSR NAGAR,MSRIT POST,BANGALORE - 560054."),
        (28, "E060IE", "INFORMATION SCIENCE AND ENGINEERING", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "Dr. Ambedkar Institute of Technology, Bangalore(AUTONOMOUS) OUTER RING ROAD,NEAR JNANA BHARATHI CAMPUS,MALLATHAHALLI,BANGALORE-560056"),
        (29, "E060CB", "COMPUTER SCIENCE AND BUSINESS SYSTEMS", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "Dr. Ambedkar Institute of Technology, Bangalore(AUTONOMOUS) OUTER RING ROAD,NEAR JNANA BHARATHI CAMPUS,MALLATHAHALLI,BANGALORE-560056"),
        (30, "E060EC", "ELECTRONICS AND COMMUNICATION ENGG", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "Dr. Ambedkar Institute of Technology, Bangalore(AUTONOMOUS) OUTER RING ROAD,NEAR JNANA BHARATHI CAMPUS,MALLATHAHALLI,BANGALORE-560056"),
        (31, "E241BT", "BIO-TECHNOLOGY", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "KLE Technological University(Formerly (BVBCET) BVBHOOMARADDI COLLEGE CAMPUS, VIDYANAGAR, HUBBALLI"),
        (32, "E007MD", "MEDICAL ELECTRONICS ENGINEERING", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "Dayananda Sagar College of Engineering, Bangalore(AUTONOMOUS) SHAVIGE MALLESHWARA HILLS, KUMARASWAMY LAYOUT, BANGALORE-560078"),
        (33, "E060AE", "AERONAUTICAL ENGINEERING", "1,12,410 - One Lakh Twelve Thousand Four Hundred and Ten", "Dr. Ambedkar Institute of Technology, Bangalore(AUTONOMOUS) OUTER RING ROAD,NEAR JNANA BHARATHI CAMPUS,MALLATHAHALLI,BANGALORE-560056")
    ]
    
    def clean_college_name(full_name):
        """Extract clean college name from full address"""
        if not full_name:
            return ""
        
        # Split by comma and take the first part
        parts = full_name.split(',')
        clean_name = parts[0].strip()
        
        # Remove (AUTONOMOUS) suffix if present
        clean_name = clean_name.replace('(AUTONOMOUS)', '').strip()
        
        return clean_name
    
    # Convert to DataFrame
    df_data = []
    for option_no, college_code, course_name, course_fee, college_name in option_entries:
        df_data.append({
            'Option_No': option_no,
            'College_Code': college_code,
            'Course_Name': course_name,
            'Course_Fee': course_fee,
            'College_Name': college_name,
            'College_Name_Clean': clean_college_name(college_name)
        })
    
    df = pd.DataFrame(df_data)
    
    # Save to CSV
    output_file = 'data/option_entries.csv'
    df.to_csv(output_file, index=False)
    
    print("🚀 Starting Updated PDF Data Processing...")
    print("=" * 60)
    print(f"✅ SUCCESS! Processed 33 option entries from user data")
    print("=" * 60)
    print("📊 Data Summary:")
    print(f"  Total entries: {len(df)}")
    print(f"  Option range: {df['Option_No'].min()} to {df['Option_No'].max()}")
    print(f"  Unique colleges: {df['College_Name_Clean'].nunique()}")
    print(f"  Unique courses: {df['Course_Name'].nunique()}")
    
    print("\n📋 Columns:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    
    print(f"\n💾 Saved to: {output_file}")
    
    print("\n📝 All 33 Option Entries:")
    print("-" * 80)
    for _, row in df.iterrows():
        print(f"{row['Option_No']:2d}. {row['College_Code']:6s} | {row['Course_Name'][:35]:35s} | {row['College_Name_Clean']}")
    
    return df

if __name__ == "__main__":
    df = parse_user_provided_data()
    print(f"\n✅ Complete! All {len(df)} entries processed successfully.")
