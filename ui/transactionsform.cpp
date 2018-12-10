#include "transactionsform.h"
#include "ui_transactionsform.h"

TransactionsForm::TransactionsForm(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::TransactionsForm)
{
    ui->setupUi(this);
}

TransactionsForm::~TransactionsForm()
{
    delete ui;
}
