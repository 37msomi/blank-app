import pool, { query } from './index';

export async function runMigrations() {
  const client = await pool.connect();
  try {
    console.log('Running migrations...');

    // Create extensions
    await client.query('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"');

    // Create employees table
    await client.query(`
      CREATE TABLE IF NOT EXISTS employees (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        department VARCHAR(255) NOT NULL,
        position VARCHAR(255) NOT NULL,
        manager_id UUID REFERENCES employees(id),
        role VARCHAR(50) NOT NULL DEFAULT 'EMPLOYEE',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);

    // Create leave_types table
    await client.query(`
      CREATE TABLE IF NOT EXISTS leave_types (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        name VARCHAR(255) NOT NULL UNIQUE,
        max_days INTEGER NOT NULL,
        requires_approval BOOLEAN DEFAULT TRUE,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);

    // Create leave_balances table
    await client.query(`
      CREATE TABLE IF NOT EXISTS leave_balances (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        employee_id UUID NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
        leave_type_id UUID NOT NULL REFERENCES leave_types(id) ON DELETE CASCADE,
        allowed_days INTEGER NOT NULL,
        used_days INTEGER NOT NULL DEFAULT 0,
        year INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(employee_id, leave_type_id, year)
      )
    `);

    // Create leave_requests table
    await client.query(`
      CREATE TABLE IF NOT EXISTS leave_requests (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        employee_id UUID NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
        leave_type_id UUID NOT NULL REFERENCES leave_types(id),
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        reason TEXT,
        status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
        approver_id UUID REFERENCES employees(id),
        rejection_reason TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);

    // Create departments table
    await client.query(`
      CREATE TABLE IF NOT EXISTS departments (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        name VARCHAR(255) NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);

    console.log('Migrations completed successfully');
  } catch (error) {
    console.error('Migration error:', error);
    throw error;
  } finally {
    client.release();
  }
}

// Seed initial data
export async function seedData() {
  try {
    console.log('Seeding data...');

    // Check if data already exists
    const checkRes = await query('SELECT COUNT(*) FROM employees');
    if (parseInt(checkRes.rows[0].count) > 0) {
      console.log('Data already exists, skipping seed');
      return;
    }

    // Insert leave types
    const leaveTypesRes = await query(`
      INSERT INTO leave_types (name, max_days, requires_approval, description)
      VALUES 
        ('Annual', 20, true, 'Annual paid leave'),
        ('Sick Leave', 10, false, 'Sick leave'),
        ('Personal', 5, true, 'Personal leave')
      RETURNING id, name
    `);

    // Insert departments
    const departmentsRes = await query(`
      INSERT INTO departments (name)
      VALUES ('Engineering'), ('Sales'), ('HR'), ('Finance')
      RETURNING id, name
    `);

    // Insert sample employees
    const departmentId = departmentsRes.rows[0].id;
    const empRes = await query(`
      INSERT INTO employees (name, email, password_hash, department, position, role)
      VALUES 
        ('Alice Johnson', 'emp@test.com', 'hashedpassword', 'Engineering', 'Engineer', 'EMPLOYEE'),
        ('Bob Manager', 'mgr@test.com', 'hashedpassword', 'Engineering', 'Manager', 'MANAGER'),
        ('Carol Admin', 'admin@test.com', 'hashedpassword', 'HR', 'HR Manager', 'ADMIN'),
        ('David Engineer', 'david@test.com', 'hashedpassword', 'Sales', 'Sales Rep', 'EMPLOYEE')
      RETURNING id, name, email
    `);

    console.log('Sample data seeded successfully');
  } catch (error) {
    console.error('Seed error:', error);
  }
}
