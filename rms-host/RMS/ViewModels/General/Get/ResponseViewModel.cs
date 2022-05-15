using System.Collections.Generic;
using RMS.Enums;

namespace RMS.ViewModels.General.Get
{
    public class ResponseViewModel
    {
        public string FirstName { get; set; }
        
        public string LastName { get; set; }

        public string EmailAddress { get; set; }
        
        public string Address { get; set; }

        public string ProfilePicture { get; set; }

        public string Role { get; set; }

        public string CompanyName { get; set; }

        public string CompanyColor { get; set; }

        public string CompanyLogo { get; set; }

        public List<string> Modules { get; set; }
    }
}