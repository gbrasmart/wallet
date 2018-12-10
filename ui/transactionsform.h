#ifndef TRANSACTIONSFORM_H
#define TRANSACTIONSFORM_H

#include <QWidget>

namespace Ui {
class TransactionsForm;
}

class TransactionsForm : public QWidget
{
    Q_OBJECT

public:
    explicit TransactionsForm(QWidget *parent = nullptr);
    ~TransactionsForm();

private:
    Ui::TransactionsForm *ui;
};

#endif // TRANSACTIONSFORM_H
