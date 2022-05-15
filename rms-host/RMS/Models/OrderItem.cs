using System;
using System.Collections.Generic;

namespace RMS.Models
{
    public class OrderItem
    {
        public int Id { get; set; }
        
        public int ProductId { get; set; }
        
        public int OrderId { get; set; }

        public virtual Product Product { get; set; }
        
        public virtual Order Order { get; set; }
        
        public virtual List<OrderItemSettings> Settings { get; set; }
    }
}