from semantic_kernel.functions import kernel_function

class EmailPlugin:
    
    @kernel_function(
        description="Send an expense claim email to the expenses team.",
    )
    def send_expense_email(self, to:str, user:str, subject:str):
        body = f"""
        To: {to}
        Subject: {subject}

        Dear Expenses Team,

        Please find attached the itemised expense claim for {user}.

        Regards,
        {user}
        """
        print(body)
        return body
