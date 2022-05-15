using System;
using System.Collections.Generic;
using RMS.Enums;

namespace RMS.Models
{
    public class Order
    {
        public int Id { get; set; }
        
        public int ForCompanyId { get; set; }
        
        public OrderStatus Status { get; set; }
        
        public DateTime PlacedDate { get; set; }

        public virtual List<CustomerDetails> CustomerDetails { get; set; }
        
        public virtual List<OrderItem> Items { get; set; }
        
        public virtual Company ForCompany { get; set; }
    }
}