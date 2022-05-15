using System;

namespace RMS.Models
{
    public class CustomerDetails
    {
        public int Id { get; set; }
        
        public string Key { get; set; }
        
        public string Value { get; set; }
        
        public int OrderId { get; set; }

        public virtual Order Order { get; set; }
    }
}