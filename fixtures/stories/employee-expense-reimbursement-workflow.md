## 🧾 **Story: Employee Expense Reimbursement Workflow**

### 📌 **Step 1: Starting the Process**
An employee begins the process by triggering the **"Start Expense Request"** event. This signals the start of an expense claim process.

> 📄 *Documentation*: “Triggered when employee initiates an expense claim.”

The process immediately moves to the next step.

---

### 📝 **Step 2: Submit Expense Request**
The employee is presented with a user task: **"Submit Expense Request"**.

- 🧑 **Assignee**: The employee who started the process (referred to as `initiator`).
- 🧾 **Form used**: `form_expense_submission`
- 🔄 **Inputs collected**:
  - `amount` (from `variables.amount`)
  - `description`
  - `date`
  - `receipt`
- 📤 **Outputs produced**:
  - An object `expenseRequest` containing amount, description, and receipt.
  - A flag `requestSubmitted = true` to confirm submission.

Once the form is submitted, the system proceeds to decision-making based on the amount.

---

### 🔀 **Step 3: Check Expense Amount**
A **gateway** labeled **"Check Expense Amount"** determines which approval path to follow:

- 🧮 **Condition 1**: If `expenseRequest.amount <= 1000`  
  → Go to **Manager Approval**
- 🧮 **Condition 2**: If `expenseRequest.amount > 1000`  
  → Go to **Finance Approval**

---

### 👨‍💼 **Path A: Manager Approval (for ≤ 1000 QAR)**
If the amount is **1000 or less**, the request is sent for **managerial review**:

- 🧑 **Assignee**: Users in `manager_group`
- 📄 **Form**: `form_manager_review`
- 🔄 **Inputs/Outputs**:
  - Input: `expenseRequest`
  - Output: `managerDecision` object containing `approved` and `comments`

Now, based on the manager’s decision, the workflow splits again.

#### 🔄 **Gateway: Based on Manager’s Decision**
- ✅ If `managerDecision.approved == true`  
  → Continue to **"Process Reimbursement"**
- ❌ If `managerDecision.approved == false`  
  → End the process with **"Request Rejected"**

---

### 👩‍💼 **Path B: Finance Approval (for > 1000 QAR)**
If the amount exceeds 1000, the request goes to **finance**:

- 🧑 **Assignee**: Users in `finance_group`
- 📄 **Form**: `form_finance_review`
- 🔄 **Outputs**:
  - `approved` and `comments` (bound to `financeDecision` implicitly in the next steps)

A gateway evaluates the finance decision:

#### 🔄 **Gateway: Based on Finance’s Decision**
- ✅ If `financeDecision.approved == true`  
  → Continue to **"Process Reimbursement"**
- ❌ If `financeDecision.approved == false`  
  → End with **"Request Rejected"**

---

### 💰 **Step: Process Reimbursement**
This is a **service task** (automated system step) where the expense is reimbursed.

- 🧠 **Service Type**: `SendPaymentToAccounting` (defined via Zeebe)
- 🔄 **Inputs**:
  - For manager path: `expenseRequest`
  - For finance path: `request = variables.expenseRequest`
- 🔄 **Outputs**:
  - For manager path: `paymentStatus`
  - For finance path: `success` mapped to `paymentStatus`

After processing payment, the process ends with confirmation.

---

### ✅ **End Events**
The process can end in one of three ways:

1. **Reimbursement Completed** (manager route)
2. **Reimbursement Completed** (finance route)
3. **Request Rejected** (from either manager or finance)

Each end event is clearly labeled and linked to its respective flow.

---

## ✅ **Summary of Key Logic**
| Condition                             | Task                    | Next Step                             |
|--------------------------------------|-------------------------|----------------------------------------|
| Amount ≤ 1000                        | Manager Approval        | If approved → Process Payment         |
| Amount > 1000                        | Finance Approval        | If approved → Process Payment         |
| Decision not approved (any case)     | N/A                     | End with Rejection                    |
| Decision approved                    | Process Reimbursement   | End with Reimbursement Completed      |

---

This process ensures that **small expenses go through a lighter managerial review**, while **larger expenses undergo stricter financial approval**. Automated service tasks are responsible for handling the **payment processing**, ensuring a clear and auditable flow of events.
