{
    'name':'Module Custom Purchase',
    'version': '17.0',
    'category': 'Purchase',
    'summary' : 'Purchase Custom Module',
    'description' : """Purchase Custom Module by Rifqi Ammar Ramadhan""",
    'website' : '',
    'author' : 'Rifqi Ammar Ramadhan',
    'depends' : ['web','base','product'],
    'data' : [
        'security/ir.model.access.csv',
        'views/autodidak_purchase_view.xml',
        'views/autodidak_purchase_action.xml',
        'views/autodidak_purchase_menuitem.xml',
        'views/autodidak_purchase_sequence.xml',
        # 'reports/autodidak_report_pdf.xml',
        'reports/autodidak_report_pdf_template.xml',
        
    ],
    'installable' : True,
    'license' : 'OEEL-1'
}