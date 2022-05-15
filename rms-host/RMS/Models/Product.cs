using System;
using System.Collections.Generic;

namespace RMS.Models
{
    public class Product
    {
        public int Id { get; set; }

        public string Name { get; set; }

        public float BasePrice { get; set; }

        public string Description { get; set; }

        public string Image { get; set; }

        public int CompanyId { get; set; }

        public virtual Company Company { get; set; }
        
        public virtual List<OrderItem> Orders { get; set; }
    }
}