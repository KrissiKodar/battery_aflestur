namespace OssurBatteryReader
{
    partial class MainForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.ControlGroupBox = new System.Windows.Forms.GroupBox();
            this.StatusButton = new System.Windows.Forms.Button();
            this.ResetButton = new System.Windows.Forms.Button();
            this.RefreshButton = new System.Windows.Forms.Button();
            this.COMPortsComboBox = new System.Windows.Forms.ComboBox();
            this.ConnectButton = new System.Windows.Forms.Button();
            this.CommunicationGroupBox = new System.Windows.Forms.GroupBox();
            this.SendButton = new System.Windows.Forms.Button();
            this.SendComboBox = new System.Windows.Forms.ComboBox();
            this.CommunicationTextBox = new System.Windows.Forms.TextBox();
            this.MenuStrip = new System.Windows.Forms.MenuStrip();
            this.AboutToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.DebugGroupBox = new System.Windows.Forms.GroupBox();
            this.ReadROMButton = new System.Windows.Forms.Button();
            this.RegisterLabelRead = new System.Windows.Forms.Label();
            this.ReadLabel = new System.Windows.Forms.Label();
            this.ReadRegisterComboBox = new System.Windows.Forms.ComboBox();
            this.ReadByteButton = new System.Windows.Forms.Button();
            this.ReadWordButton = new System.Windows.Forms.Button();
            this.ReadBlockButton = new System.Windows.Forms.Button();
            this.ReadDataTextBox = new System.Windows.Forms.TextBox();
            this.RegisterLabelWrite = new System.Windows.Forms.Label();
            this.WriteLabel = new System.Windows.Forms.Label();
            this.WriteRegisterComboBox = new System.Windows.Forms.ComboBox();
            this.WriteByteButton = new System.Windows.Forms.Button();
            this.WriteWordButton = new System.Windows.Forms.Button();
            this.WriteBlockButton = new System.Windows.Forms.Button();
            this.WriteDataTextBox = new System.Windows.Forms.TextBox();
            this.ScanSMBusButton = new System.Windows.Forms.Button();
            this.SMBusRegisterDumpButton = new System.Windows.Forms.Button();
            this.RegStartTextBox = new System.Windows.Forms.TextBox();
            this.RegEndTextBox = new System.Windows.Forms.TextBox();
            this.DashLabel = new System.Windows.Forms.Label();
            this.SMBusAddressComboBox = new System.Windows.Forms.ComboBox();
            this.SMBusAddressSelectButton = new System.Windows.Forms.Button();
            this.WordByteOrderComboBox = new System.Windows.Forms.ComboBox();
            this.WordByteOrderLabel = new System.Windows.Forms.Label();
            this.WordByteOrderOKButton = new System.Windows.Forms.Button();
            this.ToolsGroupBox = new System.Windows.Forms.GroupBox();
            this.product_type = new System.Windows.Forms.GroupBox();
            this.navi = new System.Windows.Forms.RadioButton();
            this.rheo = new System.Windows.Forms.RadioButton();
            this.powerknee = new System.Windows.Forms.RadioButton();
            this.ControlGroupBox.SuspendLayout();
            this.CommunicationGroupBox.SuspendLayout();
            this.MenuStrip.SuspendLayout();
            this.DebugGroupBox.SuspendLayout();
            this.ToolsGroupBox.SuspendLayout();
            this.product_type.SuspendLayout();
            this.SuspendLayout();
            // 
            // ControlGroupBox
            // 
            this.ControlGroupBox.Controls.Add(this.StatusButton);
            this.ControlGroupBox.Controls.Add(this.ResetButton);
            this.ControlGroupBox.Controls.Add(this.RefreshButton);
            this.ControlGroupBox.Controls.Add(this.COMPortsComboBox);
            this.ControlGroupBox.Controls.Add(this.ConnectButton);
            this.ControlGroupBox.Location = new System.Drawing.Point(14, 298);
            this.ControlGroupBox.Name = "ControlGroupBox";
            this.ControlGroupBox.Size = new System.Drawing.Size(370, 62);
            this.ControlGroupBox.TabIndex = 5;
            this.ControlGroupBox.TabStop = false;
            this.ControlGroupBox.Text = "Control";
            // 
            // StatusButton
            // 
            this.StatusButton.Enabled = false;
            this.StatusButton.Location = new System.Drawing.Point(251, 19);
            this.StatusButton.Name = "StatusButton";
            this.StatusButton.Size = new System.Drawing.Size(50, 25);
            this.StatusButton.TabIndex = 4;
            this.StatusButton.Text = "Status";
            this.StatusButton.UseVisualStyleBackColor = true;
            this.StatusButton.Click += new System.EventHandler(this.StatusButton_Click);
            // 
            // ResetButton
            // 
            this.ResetButton.Enabled = false;
            this.ResetButton.Location = new System.Drawing.Point(306, 19);
            this.ResetButton.Name = "ResetButton";
            this.ResetButton.Size = new System.Drawing.Size(50, 25);
            this.ResetButton.TabIndex = 3;
            this.ResetButton.Text = "Reset";
            this.ResetButton.UseVisualStyleBackColor = true;
            this.ResetButton.Click += new System.EventHandler(this.ResetButton_Click);
            // 
            // RefreshButton
            // 
            this.RefreshButton.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.RefreshButton.Location = new System.Drawing.Point(156, 19);
            this.RefreshButton.Name = "RefreshButton";
            this.RefreshButton.Size = new System.Drawing.Size(55, 25);
            this.RefreshButton.TabIndex = 2;
            this.RefreshButton.Text = "Refresh";
            this.RefreshButton.UseVisualStyleBackColor = true;
            this.RefreshButton.Click += new System.EventHandler(this.RefreshButton_Click);
            // 
            // COMPortsComboBox
            // 
            this.COMPortsComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.COMPortsComboBox.Font = new System.Drawing.Font("Courier New", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(238)));
            this.COMPortsComboBox.FormattingEnabled = true;
            this.COMPortsComboBox.Location = new System.Drawing.Point(90, 20);
            this.COMPortsComboBox.Name = "COMPortsComboBox";
            this.COMPortsComboBox.Size = new System.Drawing.Size(60, 23);
            this.COMPortsComboBox.TabIndex = 1;
            this.COMPortsComboBox.SelectedIndexChanged += new System.EventHandler(this.COMPortsComboBox_SelectedIndexChanged);
            // 
            // ConnectButton
            // 
            this.ConnectButton.Location = new System.Drawing.Point(9, 19);
            this.ConnectButton.Name = "ConnectButton";
            this.ConnectButton.Size = new System.Drawing.Size(75, 25);
            this.ConnectButton.TabIndex = 0;
            this.ConnectButton.Text = "Connect";
            this.ConnectButton.UseVisualStyleBackColor = true;
            this.ConnectButton.Click += new System.EventHandler(this.ConnectButton_Click);
            // 
            // CommunicationGroupBox
            // 
            this.CommunicationGroupBox.Controls.Add(this.SendButton);
            this.CommunicationGroupBox.Controls.Add(this.SendComboBox);
            this.CommunicationGroupBox.Controls.Add(this.CommunicationTextBox);
            this.CommunicationGroupBox.Location = new System.Drawing.Point(11, 27);
            this.CommunicationGroupBox.Name = "CommunicationGroupBox";
            this.CommunicationGroupBox.Size = new System.Drawing.Size(700, 265);
            this.CommunicationGroupBox.TabIndex = 4;
            this.CommunicationGroupBox.TabStop = false;
            this.CommunicationGroupBox.Text = "Communication";
            // 
            // SendButton
            // 
            this.SendButton.Location = new System.Drawing.Point(647, 237);
            this.SendButton.Name = "SendButton";
            this.SendButton.Size = new System.Drawing.Size(51, 25);
            this.SendButton.TabIndex = 2;
            this.SendButton.Text = "Send";
            this.SendButton.UseVisualStyleBackColor = true;
            this.SendButton.Click += new System.EventHandler(this.SendButton_Click);
            // 
            // SendComboBox
            // 
            this.SendComboBox.Font = new System.Drawing.Font("Courier New", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(238)));
            this.SendComboBox.FormattingEnabled = true;
            this.SendComboBox.Location = new System.Drawing.Point(3, 238);
            this.SendComboBox.Name = "SendComboBox";
            this.SendComboBox.Size = new System.Drawing.Size(643, 23);
            this.SendComboBox.TabIndex = 1;
            this.SendComboBox.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.SendComboBox_KeyPress);
            // 
            // CommunicationTextBox
            // 
            this.CommunicationTextBox.BackColor = System.Drawing.SystemColors.Window;
            this.CommunicationTextBox.Font = new System.Drawing.Font("Courier New", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(238)));
            this.CommunicationTextBox.Location = new System.Drawing.Point(3, 12);
            this.CommunicationTextBox.Multiline = true;
            this.CommunicationTextBox.Name = "CommunicationTextBox";
            this.CommunicationTextBox.ReadOnly = true;
            this.CommunicationTextBox.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.CommunicationTextBox.Size = new System.Drawing.Size(694, 220);
            this.CommunicationTextBox.TabIndex = 0;
            // 
            // MenuStrip
            // 
            this.MenuStrip.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.AboutToolStripMenuItem});
            this.MenuStrip.Location = new System.Drawing.Point(0, 0);
            this.MenuStrip.Name = "MenuStrip";
            this.MenuStrip.Size = new System.Drawing.Size(752, 24);
            this.MenuStrip.TabIndex = 7;
            this.MenuStrip.Text = "menuStrip1";
            // 
            // AboutToolStripMenuItem
            // 
            this.AboutToolStripMenuItem.Name = "AboutToolStripMenuItem";
            this.AboutToolStripMenuItem.Size = new System.Drawing.Size(52, 20);
            this.AboutToolStripMenuItem.Text = "About";
            this.AboutToolStripMenuItem.Click += new System.EventHandler(this.AboutToolStripMenuItem_Click);
            // 
            // DebugGroupBox
            // 
            this.DebugGroupBox.Controls.Add(this.ReadROMButton);
            this.DebugGroupBox.Location = new System.Drawing.Point(390, 299);
            this.DebugGroupBox.Name = "DebugGroupBox";
            this.DebugGroupBox.Size = new System.Drawing.Size(103, 61);
            this.DebugGroupBox.TabIndex = 8;
            this.DebugGroupBox.TabStop = false;
            this.DebugGroupBox.Text = "Read DataFlash";
            this.DebugGroupBox.Enter += new System.EventHandler(this.DebugGroupBox_Enter);
            // 
            // ReadROMButton
            // 
            this.ReadROMButton.Location = new System.Drawing.Point(6, 21);
            this.ReadROMButton.Name = "ReadROMButton";
            this.ReadROMButton.Size = new System.Drawing.Size(75, 23);
            this.ReadROMButton.TabIndex = 0;
            this.ReadROMButton.Text = "Read DF";
            this.ReadROMButton.UseVisualStyleBackColor = true;
            this.ReadROMButton.Click += new System.EventHandler(this.ReadROMButton_Click);
            // 
            // RegisterLabelRead
            // 
            this.RegisterLabelRead.AutoSize = true;
            this.RegisterLabelRead.Location = new System.Drawing.Point(7, 55);
            this.RegisterLabelRead.Name = "RegisterLabelRead";
            this.RegisterLabelRead.Size = new System.Drawing.Size(49, 13);
            this.RegisterLabelRead.TabIndex = 1;
            this.RegisterLabelRead.Text = "Register:";
            // 
            // ReadLabel
            // 
            this.ReadLabel.AutoSize = true;
            this.ReadLabel.Location = new System.Drawing.Point(108, 55);
            this.ReadLabel.Name = "ReadLabel";
            this.ReadLabel.Size = new System.Drawing.Size(36, 13);
            this.ReadLabel.TabIndex = 8;
            this.ReadLabel.Text = "Read:";
            // 
            // ReadRegisterComboBox
            // 
            this.ReadRegisterComboBox.DropDownHeight = 93;
            this.ReadRegisterComboBox.Font = new System.Drawing.Font("Courier New", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(238)));
            this.ReadRegisterComboBox.FormattingEnabled = true;
            this.ReadRegisterComboBox.IntegralHeight = false;
            this.ReadRegisterComboBox.Location = new System.Drawing.Point(59, 51);
            this.ReadRegisterComboBox.Name = "ReadRegisterComboBox";
            this.ReadRegisterComboBox.Size = new System.Drawing.Size(38, 23);
            this.ReadRegisterComboBox.TabIndex = 3;
            this.ReadRegisterComboBox.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.ReadRegisterComboBox_KeyPress);
            // 
            // ReadByteButton
            // 
            this.ReadByteButton.Location = new System.Drawing.Point(222, 50);
            this.ReadByteButton.Name = "ReadByteButton";
            this.ReadByteButton.Size = new System.Drawing.Size(42, 25);
            this.ReadByteButton.TabIndex = 5;
            this.ReadByteButton.Text = "byte";
            this.ReadByteButton.UseVisualStyleBackColor = true;
            this.ReadByteButton.Click += new System.EventHandler(this.ReadByteButton_Click);
            // 
            // ReadWordButton
            // 
            this.ReadWordButton.Location = new System.Drawing.Point(268, 50);
            this.ReadWordButton.Name = "ReadWordButton";
            this.ReadWordButton.Size = new System.Drawing.Size(42, 25);
            this.ReadWordButton.TabIndex = 9;
            this.ReadWordButton.Text = "word";
            this.ReadWordButton.UseVisualStyleBackColor = true;
            this.ReadWordButton.Click += new System.EventHandler(this.ReadWordButton_Click);
            // 
            // ReadBlockButton
            // 
            this.ReadBlockButton.Location = new System.Drawing.Point(314, 50);
            this.ReadBlockButton.Name = "ReadBlockButton";
            this.ReadBlockButton.Size = new System.Drawing.Size(42, 25);
            this.ReadBlockButton.TabIndex = 10;
            this.ReadBlockButton.Text = "block";
            this.ReadBlockButton.UseVisualStyleBackColor = true;
            this.ReadBlockButton.Click += new System.EventHandler(this.ReadBlockButton_Click);
            // 
            // ReadDataTextBox
            // 
            this.ReadDataTextBox.BackColor = System.Drawing.SystemColors.Window;
            this.ReadDataTextBox.Font = new System.Drawing.Font("Courier New", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(238)));
            this.ReadDataTextBox.Location = new System.Drawing.Point(147, 51);
            this.ReadDataTextBox.Multiline = true;
            this.ReadDataTextBox.Name = "ReadDataTextBox";
            this.ReadDataTextBox.ReadOnly = true;
            this.ReadDataTextBox.Size = new System.Drawing.Size(69, 23);
            this.ReadDataTextBox.TabIndex = 11;
            // 
            // RegisterLabelWrite
            // 
            this.RegisterLabelWrite.AutoSize = true;
            this.RegisterLabelWrite.Location = new System.Drawing.Point(7, 84);
            this.RegisterLabelWrite.Name = "RegisterLabelWrite";
            this.RegisterLabelWrite.Size = new System.Drawing.Size(49, 13);
            this.RegisterLabelWrite.TabIndex = 12;
            this.RegisterLabelWrite.Text = "Register:";
            // 
            // WriteLabel
            // 
            this.WriteLabel.AutoSize = true;
            this.WriteLabel.Location = new System.Drawing.Point(109, 84);
            this.WriteLabel.Name = "WriteLabel";
            this.WriteLabel.Size = new System.Drawing.Size(35, 13);
            this.WriteLabel.TabIndex = 15;
            this.WriteLabel.Text = "Write:";
            // 
            // WriteRegisterComboBox
            // 
            this.WriteRegisterComboBox.DropDownHeight = 93;
            this.WriteRegisterComboBox.Font = new System.Drawing.Font("Courier New", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(238)));
            this.WriteRegisterComboBox.FormattingEnabled = true;
            this.WriteRegisterComboBox.IntegralHeight = false;
            this.WriteRegisterComboBox.Location = new System.Drawing.Point(59, 80);
            this.WriteRegisterComboBox.Name = "WriteRegisterComboBox";
            this.WriteRegisterComboBox.Size = new System.Drawing.Size(38, 23);
            this.WriteRegisterComboBox.TabIndex = 13;
            this.WriteRegisterComboBox.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.WriteRegisterComboBox_KeyPress);
            // 
            // WriteByteButton
            // 
            this.WriteByteButton.Location = new System.Drawing.Point(222, 79);
            this.WriteByteButton.Name = "WriteByteButton";
            this.WriteByteButton.Size = new System.Drawing.Size(42, 25);
            this.WriteByteButton.TabIndex = 14;
            this.WriteByteButton.Text = "byte";
            this.WriteByteButton.UseVisualStyleBackColor = true;
            this.WriteByteButton.Click += new System.EventHandler(this.WriteByteButton_Click);
            // 
            // WriteWordButton
            // 
            this.WriteWordButton.Location = new System.Drawing.Point(268, 79);
            this.WriteWordButton.Name = "WriteWordButton";
            this.WriteWordButton.Size = new System.Drawing.Size(42, 25);
            this.WriteWordButton.TabIndex = 16;
            this.WriteWordButton.Text = "word";
            this.WriteWordButton.UseVisualStyleBackColor = true;
            this.WriteWordButton.Click += new System.EventHandler(this.WriteWordButton_Click);
            // 
            // WriteBlockButton
            // 
            this.WriteBlockButton.Location = new System.Drawing.Point(314, 79);
            this.WriteBlockButton.Name = "WriteBlockButton";
            this.WriteBlockButton.Size = new System.Drawing.Size(42, 25);
            this.WriteBlockButton.TabIndex = 17;
            this.WriteBlockButton.Text = "block";
            this.WriteBlockButton.UseVisualStyleBackColor = true;
            this.WriteBlockButton.Click += new System.EventHandler(this.WriteBlockButton_Click);
            // 
            // WriteDataTextBox
            // 
            this.WriteDataTextBox.BackColor = System.Drawing.SystemColors.Window;
            this.WriteDataTextBox.Font = new System.Drawing.Font("Courier New", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(238)));
            this.WriteDataTextBox.Location = new System.Drawing.Point(147, 80);
            this.WriteDataTextBox.Multiline = true;
            this.WriteDataTextBox.Name = "WriteDataTextBox";
            this.WriteDataTextBox.Size = new System.Drawing.Size(69, 23);
            this.WriteDataTextBox.TabIndex = 18;
            this.WriteDataTextBox.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.WriteDataTextBox_KeyPress);
            // 
            // ScanSMBusButton
            // 
            this.ScanSMBusButton.Location = new System.Drawing.Point(8, 20);
            this.ScanSMBusButton.Name = "ScanSMBusButton";
            this.ScanSMBusButton.Size = new System.Drawing.Size(90, 25);
            this.ScanSMBusButton.TabIndex = 5;
            this.ScanSMBusButton.Text = "Scan SMBus";
            this.ScanSMBusButton.UseVisualStyleBackColor = true;
            this.ScanSMBusButton.Click += new System.EventHandler(this.ScanSMBusButton_Click);
            // 
            // SMBusRegisterDumpButton
            // 
            this.SMBusRegisterDumpButton.Location = new System.Drawing.Point(8, 109);
            this.SMBusRegisterDumpButton.Name = "SMBusRegisterDumpButton";
            this.SMBusRegisterDumpButton.Size = new System.Drawing.Size(90, 25);
            this.SMBusRegisterDumpButton.TabIndex = 22;
            this.SMBusRegisterDumpButton.Text = "Dump Registers";
            this.SMBusRegisterDumpButton.UseVisualStyleBackColor = true;
            this.SMBusRegisterDumpButton.Click += new System.EventHandler(this.SMBusRegisterDumpButton_Click);
            // 
            // RegStartTextBox
            // 
            this.RegStartTextBox.BackColor = System.Drawing.SystemColors.Window;
            this.RegStartTextBox.Font = new System.Drawing.Font("Courier New", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(238)));
            this.RegStartTextBox.Location = new System.Drawing.Point(111, 110);
            this.RegStartTextBox.Multiline = true;
            this.RegStartTextBox.Name = "RegStartTextBox";
            this.RegStartTextBox.Size = new System.Drawing.Size(23, 23);
            this.RegStartTextBox.TabIndex = 23;
            this.RegStartTextBox.Text = "00";
            this.RegStartTextBox.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.RegStartTextBox_KeyPress);
            // 
            // RegEndTextBox
            // 
            this.RegEndTextBox.BackColor = System.Drawing.SystemColors.Window;
            this.RegEndTextBox.Font = new System.Drawing.Font("Courier New", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(238)));
            this.RegEndTextBox.Location = new System.Drawing.Point(147, 110);
            this.RegEndTextBox.Multiline = true;
            this.RegEndTextBox.Name = "RegEndTextBox";
            this.RegEndTextBox.Size = new System.Drawing.Size(23, 23);
            this.RegEndTextBox.TabIndex = 24;
            this.RegEndTextBox.Text = "20";
            this.RegEndTextBox.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.RegEndTextBox_KeyPress);
            // 
            // DashLabel
            // 
            this.DashLabel.AutoSize = true;
            this.DashLabel.Location = new System.Drawing.Point(136, 115);
            this.DashLabel.Name = "DashLabel";
            this.DashLabel.Size = new System.Drawing.Size(10, 13);
            this.DashLabel.TabIndex = 25;
            this.DashLabel.Text = "-";
            // 
            // SMBusAddressComboBox
            // 
            this.SMBusAddressComboBox.DropDownHeight = 93;
            this.SMBusAddressComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.SMBusAddressComboBox.Font = new System.Drawing.Font("Courier New", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(238)));
            this.SMBusAddressComboBox.FormattingEnabled = true;
            this.SMBusAddressComboBox.IntegralHeight = false;
            this.SMBusAddressComboBox.Location = new System.Drawing.Point(103, 21);
            this.SMBusAddressComboBox.Name = "SMBusAddressComboBox";
            this.SMBusAddressComboBox.Size = new System.Drawing.Size(38, 23);
            this.SMBusAddressComboBox.TabIndex = 26;
            // 
            // SMBusAddressSelectButton
            // 
            this.SMBusAddressSelectButton.Enabled = false;
            this.SMBusAddressSelectButton.Location = new System.Drawing.Point(146, 20);
            this.SMBusAddressSelectButton.Name = "SMBusAddressSelectButton";
            this.SMBusAddressSelectButton.Size = new System.Drawing.Size(90, 25);
            this.SMBusAddressSelectButton.TabIndex = 27;
            this.SMBusAddressSelectButton.Text = "Select Address";
            this.SMBusAddressSelectButton.UseVisualStyleBackColor = true;
            this.SMBusAddressSelectButton.Click += new System.EventHandler(this.SMBusAddressSelectButton_Click);
            // 
            // WordByteOrderComboBox
            // 
            this.WordByteOrderComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.WordByteOrderComboBox.FormattingEnabled = true;
            this.WordByteOrderComboBox.Items.AddRange(new object[] {
            "No reverse",
            "Reverse read",
            "Reverse write",
            "Reverse read/write"});
            this.WordByteOrderComboBox.Location = new System.Drawing.Point(186, 132);
            this.WordByteOrderComboBox.Name = "WordByteOrderComboBox";
            this.WordByteOrderComboBox.Size = new System.Drawing.Size(120, 21);
            this.WordByteOrderComboBox.TabIndex = 29;
            // 
            // WordByteOrderLabel
            // 
            this.WordByteOrderLabel.AutoSize = true;
            this.WordByteOrderLabel.Location = new System.Drawing.Point(183, 115);
            this.WordByteOrderLabel.Name = "WordByteOrderLabel";
            this.WordByteOrderLabel.Size = new System.Drawing.Size(86, 13);
            this.WordByteOrderLabel.TabIndex = 30;
            this.WordByteOrderLabel.Text = "Word byte-order:";
            // 
            // WordByteOrderOKButton
            // 
            this.WordByteOrderOKButton.Location = new System.Drawing.Point(314, 131);
            this.WordByteOrderOKButton.Name = "WordByteOrderOKButton";
            this.WordByteOrderOKButton.Size = new System.Drawing.Size(42, 23);
            this.WordByteOrderOKButton.TabIndex = 5;
            this.WordByteOrderOKButton.Text = "OK";
            this.WordByteOrderOKButton.UseVisualStyleBackColor = true;
            this.WordByteOrderOKButton.Click += new System.EventHandler(this.WordByteOrderOKButton_Click);
            // 
            // ToolsGroupBox
            // 
            this.ToolsGroupBox.Controls.Add(this.WordByteOrderOKButton);
            this.ToolsGroupBox.Controls.Add(this.WordByteOrderLabel);
            this.ToolsGroupBox.Controls.Add(this.WordByteOrderComboBox);
            this.ToolsGroupBox.Controls.Add(this.SMBusAddressSelectButton);
            this.ToolsGroupBox.Controls.Add(this.SMBusAddressComboBox);
            this.ToolsGroupBox.Controls.Add(this.DashLabel);
            this.ToolsGroupBox.Controls.Add(this.RegEndTextBox);
            this.ToolsGroupBox.Controls.Add(this.RegStartTextBox);
            this.ToolsGroupBox.Controls.Add(this.SMBusRegisterDumpButton);
            this.ToolsGroupBox.Controls.Add(this.ScanSMBusButton);
            this.ToolsGroupBox.Controls.Add(this.WriteDataTextBox);
            this.ToolsGroupBox.Controls.Add(this.WriteBlockButton);
            this.ToolsGroupBox.Controls.Add(this.WriteWordButton);
            this.ToolsGroupBox.Controls.Add(this.WriteByteButton);
            this.ToolsGroupBox.Controls.Add(this.WriteRegisterComboBox);
            this.ToolsGroupBox.Controls.Add(this.WriteLabel);
            this.ToolsGroupBox.Controls.Add(this.RegisterLabelWrite);
            this.ToolsGroupBox.Controls.Add(this.ReadDataTextBox);
            this.ToolsGroupBox.Controls.Add(this.ReadBlockButton);
            this.ToolsGroupBox.Controls.Add(this.ReadWordButton);
            this.ToolsGroupBox.Controls.Add(this.ReadByteButton);
            this.ToolsGroupBox.Controls.Add(this.ReadRegisterComboBox);
            this.ToolsGroupBox.Controls.Add(this.ReadLabel);
            this.ToolsGroupBox.Controls.Add(this.RegisterLabelRead);
            this.ToolsGroupBox.Enabled = false;
            this.ToolsGroupBox.Location = new System.Drawing.Point(19, 377);
            this.ToolsGroupBox.Name = "ToolsGroupBox";
            this.ToolsGroupBox.Size = new System.Drawing.Size(365, 164);
            this.ToolsGroupBox.TabIndex = 6;
            this.ToolsGroupBox.TabStop = false;
            this.ToolsGroupBox.Text = "Tools";
            // 
            // product_type
            // 
            this.product_type.Controls.Add(this.navi);
            this.product_type.Controls.Add(this.rheo);
            this.product_type.Controls.Add(this.powerknee);
            this.product_type.Location = new System.Drawing.Point(499, 298);
            this.product_type.Name = "product_type";
            this.product_type.Size = new System.Drawing.Size(128, 100);
            this.product_type.TabIndex = 9;
            this.product_type.TabStop = false;
            this.product_type.Text = "Product type";
            // 
            // navi
            // 
            this.navi.AutoSize = true;
            this.navi.Location = new System.Drawing.Point(18, 68);
            this.navi.Name = "navi";
            this.navi.Size = new System.Drawing.Size(47, 17);
            this.navi.TabIndex = 2;
            this.navi.Text = "Navi";
            this.navi.UseVisualStyleBackColor = true;
            this.navi.CheckedChanged += new System.EventHandler(this.RadioButton_CheckedChanged);
            // 
            // rheo
            // 
            this.rheo.AutoSize = true;
            this.rheo.Location = new System.Drawing.Point(18, 44);
            this.rheo.Name = "rheo";
            this.rheo.Size = new System.Drawing.Size(51, 17);
            this.rheo.TabIndex = 1;
            this.rheo.Text = "Rheo";
            this.rheo.UseVisualStyleBackColor = true;
            this.rheo.CheckedChanged += new System.EventHandler(this.RadioButton_CheckedChanged);
            // 
            // powerknee
            // 
            this.powerknee.AutoSize = true;
            this.powerknee.Location = new System.Drawing.Point(18, 20);
            this.powerknee.Name = "powerknee";
            this.powerknee.Size = new System.Drawing.Size(79, 17);
            this.powerknee.TabIndex = 0;
            this.powerknee.Text = "Powerknee";
            this.powerknee.UseVisualStyleBackColor = true;
            this.powerknee.CheckedChanged += new System.EventHandler(this.RadioButton_CheckedChanged);
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(752, 552);
            this.Controls.Add(this.product_type);
            this.Controls.Add(this.DebugGroupBox);
            this.Controls.Add(this.ToolsGroupBox);
            this.Controls.Add(this.ControlGroupBox);
            this.Controls.Add(this.CommunicationGroupBox);
            this.Controls.Add(this.MenuStrip);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MainMenuStrip = this.MenuStrip;
            this.MaximizeBox = false;
            this.Name = "MainForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Ossur Battery Reader"; //Smart Battery Hack
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.MainForm_FormClosing);
            this.Load += new System.EventHandler(this.MainForm_Load);
            this.ControlGroupBox.ResumeLayout(false);
            this.CommunicationGroupBox.ResumeLayout(false);
            this.CommunicationGroupBox.PerformLayout();
            this.MenuStrip.ResumeLayout(false);
            this.MenuStrip.PerformLayout();
            this.DebugGroupBox.ResumeLayout(false);
            this.ToolsGroupBox.ResumeLayout(false);
            this.ToolsGroupBox.PerformLayout();
            this.product_type.ResumeLayout(false);
            this.product_type.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.GroupBox ControlGroupBox;
        private System.Windows.Forms.Button StatusButton;
        private System.Windows.Forms.Button ResetButton;
        private System.Windows.Forms.Button RefreshButton;
        private System.Windows.Forms.ComboBox COMPortsComboBox;
        private System.Windows.Forms.Button ConnectButton;
        private System.Windows.Forms.GroupBox CommunicationGroupBox;
        private System.Windows.Forms.Button SendButton;
        private System.Windows.Forms.ComboBox SendComboBox;
        private System.Windows.Forms.TextBox CommunicationTextBox;
        private System.Windows.Forms.MenuStrip MenuStrip;
        private System.Windows.Forms.ToolStripMenuItem AboutToolStripMenuItem;
        private System.Windows.Forms.GroupBox DebugGroupBox;
        private System.Windows.Forms.Button ReadROMButton;
        private System.Windows.Forms.Label RegisterLabelRead;
        private System.Windows.Forms.Label ReadLabel;
        private System.Windows.Forms.ComboBox ReadRegisterComboBox;
        private System.Windows.Forms.Button ReadByteButton;
        private System.Windows.Forms.Button ReadWordButton;
        private System.Windows.Forms.Button ReadBlockButton;
        private System.Windows.Forms.TextBox ReadDataTextBox;
        private System.Windows.Forms.Label RegisterLabelWrite;
        private System.Windows.Forms.Label WriteLabel;
        private System.Windows.Forms.ComboBox WriteRegisterComboBox;
        private System.Windows.Forms.Button WriteByteButton;
        private System.Windows.Forms.Button WriteWordButton;
        private System.Windows.Forms.Button WriteBlockButton;
        private System.Windows.Forms.TextBox WriteDataTextBox;
        private System.Windows.Forms.Button ScanSMBusButton;
        private System.Windows.Forms.Button SMBusRegisterDumpButton;
        private System.Windows.Forms.TextBox RegStartTextBox;
        private System.Windows.Forms.TextBox RegEndTextBox;
        private System.Windows.Forms.Label DashLabel;
        private System.Windows.Forms.ComboBox SMBusAddressComboBox;
        private System.Windows.Forms.Button SMBusAddressSelectButton;
        private System.Windows.Forms.ComboBox WordByteOrderComboBox;
        private System.Windows.Forms.Label WordByteOrderLabel;
        private System.Windows.Forms.Button WordByteOrderOKButton;
        private System.Windows.Forms.GroupBox ToolsGroupBox;
        private System.Windows.Forms.GroupBox product_type;
        private System.Windows.Forms.RadioButton navi;
        private System.Windows.Forms.RadioButton rheo;
        private System.Windows.Forms.RadioButton powerknee;
    }
}

