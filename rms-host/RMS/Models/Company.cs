using System;
using System.Collections.Generic;

namespace RMS.Models
{
    public class Company
    {
        public int Id { get; set; }

        public string Name { get; set; }

        public string Logo { get; set; }

        public string Color { get; set; }

        public int MaxAccounts { get; set; }

        public virtual List<User> Users { get; set; }
        
        public virtual List<Product> Products { get; set; }

        public virtual List<Page> Pages { get; set; }

        public virtual List<CompanyModule> CompanyModules { get; set; }
        
        public virtual List<Order> CompanyOrders { get; set; }
    }
}