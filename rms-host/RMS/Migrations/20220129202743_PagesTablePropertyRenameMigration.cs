using Microsoft.EntityFrameworkCore.Migrations;

namespace RMS.Migrations
{
    public partial class PagesTablePropertyRenameMigration : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "MardownContent",
                table: "Pages",
                newName: "MarkdownContent");
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "MarkdownContent",
                table: "Pages",
                newName: "MardownContent");
        }
    }
}
