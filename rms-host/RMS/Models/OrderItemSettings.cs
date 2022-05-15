using System;

namespace RMS.Models
{
    public class OrderItemSettings
    {
        public int Id { get; set; }
        
        public string Key { get; set; }
        
        public string Value { get; set; }
        
        public int OrderItemId { get; set; }
        
        public virtual OrderItem Item { get; set; }
    }
}