from models.models import SystemConfig, BorrowRecord
from datetime import datetime
import json

class FeeCalculator:
    def __init__(self, db_session):
        self.db_session = db_session
        
    def get_late_fee_rate(self):
        """Get the current late fee rate from system configuration"""
        config = self.db_session.query(SystemConfig).filter_by(key='late_fee_rate').first()
        if not config:
            # Default rate of ₹5 per day if not configured
            return 5.0
        return float(config.value)
        
    def calculate_late_fee(self, borrow_record):
        """Calculate late fee for a borrow record"""
        if borrow_record.returned or not borrow_record.due_date:
            return 0.0
            
        days_overdue = (datetime.now() - borrow_record.due_date).days
        if days_overdue <= 0:
            return 0.0
            
        rate = self.get_late_fee_rate()
        return days_overdue * rate
        
    def update_late_fee_rate(self, new_rate):
        """Update the late fee rate in system configuration"""
        config = self.db_session.query(SystemConfig).filter_by(key='late_fee_rate').first()
        if not config:
            config = SystemConfig(
                key='late_fee_rate',
                value=str(new_rate),
                description='Late fee rate in Indian Rupees per day'
            )
            self.db_session.add(config)
        else:
            config.value = str(new_rate)
            
        self.db_session.commit()
        
    def process_overdue_books(self):
        """Process all overdue books and update their fines"""
        overdue_records = self.db_session.query(BorrowRecord).filter_by(
            returned=False
        ).filter(
            BorrowRecord.due_date < datetime.now()
        ).all()
        
        for record in overdue_records:
            record.fine = self.calculate_late_fee(record)
            
        self.db_session.commit()
        
    def get_fee_summary(self, user_id):
        """Get a summary of fees for a user"""
        records = self.db_session.query(BorrowRecord).filter_by(
            user_id=user_id,
            returned=True
        ).filter(
            BorrowRecord.fine > 0
        ).all()
        
        total_fees = sum(record.fine for record in records)
        paid_fees = sum(record.fine for record in records if record.fine_paid)
        unpaid_fees = total_fees - paid_fees
        
        return {
            'total_fees': total_fees,
            'paid_fees': paid_fees,
            'unpaid_fees': unpaid_fees,
            'records': records
        }
        
    def mark_fee_as_paid(self, borrow_record_id):
        """Mark a fee as paid for a borrow record"""
        record = self.db_session.query(BorrowRecord).get(borrow_record_id)
        if record:
            record.fine_paid = True
            self.db_session.commit()
            return True
        return False 