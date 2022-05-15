using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.Mail;
using System.Text;

namespace RMS.services
{
    public static class EmailingService
    {
        public static bool SendEmail(string toEmail, string subject, string body)
        {
            // Create an SMTP server connection with Google
            SmtpClient client = new SmtpClient("smtp.office365.com", 587);
            
            // Credentials for logging in
            NetworkCredential credentials = new NetworkCredential(SettingsService.EmailAddress, SettingsService.EmailPassword);  
            
            // Connect to the SMTP server
            client.EnableSsl = true;  
            client.UseDefaultCredentials = false;  
            client.Credentials = credentials;   
            
            var to = toEmail;
            var from = SettingsService.EmailAddress;
            
            var message = new MailMessage(from, to);
            message.Subject = subject;  
            message.Body = body;  
            message.BodyEncoding = Encoding.UTF8;  
            message.IsBodyHtml = true;
            
            try   
            {  
                client.Send(message);
                return true;
            }
            catch (Exception)
            {
                return false;
            }  
        }

        public static bool SendTemplate(string template, Dictionary<string, string> settings)
        {
            // Send the template in an email
            return SendEmail(settings["email"], settings["subject"], EvaluateTemplate(template, settings));
        }

        public static string EvaluateTemplate(string template, Dictionary<string, string> settings)
        {
            // Get the template from the templates/emails folder by name in project root
            var templatePath = Path.Combine(Directory.GetCurrentDirectory(), "Templates", "Emails", template);
            
            // Read the template into a string
            string templateString = File.ReadAllText(templatePath);
            
            // Replace the settings in the template
            foreach (var setting in settings)
                templateString = templateString.Replace($"{{{setting.Key}}}", setting.Value);

            return templateString;
        }
    }
}