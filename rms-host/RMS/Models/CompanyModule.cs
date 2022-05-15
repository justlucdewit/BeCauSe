using System;

namespace RMS.Models
{
    public class CompanyModule
    {
        public int Id { get; set; }

        public int CompanyId { get; set; }

        public string Module { get; set; }
        
        public virtual Company Company { get; set; }
    }
}